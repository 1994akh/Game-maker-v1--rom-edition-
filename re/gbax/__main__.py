"""Command-line entry point: python -m gbax <command> ROM [options]. See gbax/__init__.py and PROCEDURE.md."""
import argparse
import csv
import json
import sys
import time

from . import extract as extract_mod
from . import scan as scan_mod
from . import sigs as sigs_mod
from .rom import ROOT, Rom


def cmd_identify(rom, args):
    stubs, _ = scan_mod.bios_calls(rom.data)
    matches, inferred = sigs_mod.match(rom.data, ["pokefirered_sdk"]) if (sigs_mod.SIGDB / "pokefirered_sdk.json").exists() \
        else ([], {})
    m4a = sorted({m[0] for m in matches if m[1].startswith("m4a") and m[5]})
    info = {
        "file": str(rom.path), "size": rom.size, "title": rom.title, "code": rom.code, "maker": rom.maker,
        "version": rom.version, "header_checksum_ok": rom.header_ok, "sha1": rom.sha1, "crc32": rom.crc32,
        "known_as": rom.known_as, "save_type": rom.save_types(), "bios_stubs": sorted(stubs),
        "sound_engine": ("MP2K/M4A (Nintendo SDK)" if m4a else "not MP2K, or a variant gbax can't fingerprint yet"),
        "m4a_functions_found": len(m4a), "song_table": f"0x{inferred['gSongTable']:08X}" if "gSongTable" in inferred else None,
        "workspace": str(rom.workspace),
    }
    if "gSongTable" in inferred:
        from . import music
        songs = music.read_song_table(rom, inferred["gSongTable"])
        music.write_song_list(rom, songs)
        info["songs"] = len(songs)
        info["songs_with_tracks"] = sum(1 for s in songs if s["tracks"])
        info["voicegroups"] = len({s["voicegroup"] for s in songs if s["voicegroup"]})
    rom.write_json("identify.json", info)
    return info


def cmd_scan(rom, args):
    t0 = time.time()
    r = scan_mod.scan(rom, deep=args.deep)
    ws = rom.workspace
    with open(ws / "blobs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["address", "compression", "size", "compressed_size"])
        for off, kind, size, clen, _ in r["blobs"]:
            w.writerow([f"0x{off + 0x08000000:08X}", kind, size, clen])
    with open(ws / "pointer_tables.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["address", "entries"])
        for s, n in r["pointer_tables"]:
            w.writerow([f"0x{s + 0x08000000:08X}", n])
    with open(ws / "regions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["address", "entropy_bits", "ff_fraction", "zero_fraction"])
        for s, e, ff, z in r["entropy"]:
            w.writerow([f"0x{s + 0x08000000:08X}", f"{e:.2f}", f"{ff:.2f}", f"{z:.2f}"])
    summary = {
        "pointers": r["pointers"], "pointer_targets": r["pointer_targets"],
        "pointer_tables": len(r["pointer_tables"]), "largest_pointer_tables": sorted(
            ({"address": f"0x{s + 0x08000000:08X}", "entries": n} for s, n in r["pointer_tables"]),
            key=lambda t: -t["entries"])[:10],
        "thumb_bl_calls": r["bl_calls"], "function_seeds": len(r["function_seeds"]),
        "veneers": len(r["veneers"]), "master_table_candidates": r["master_tables"],
        "compressed_blobs": {k: sum(1 for b in r["blobs"] if b[1] == k) for k in {b[1] for b in r["blobs"]}},
        "compressed_bytes_decoded": sum(b[2] for b in r["blobs"]),
        "free_space_runs": [{"address": f"0x{s + 0x08000000:08X}", "length": n, "fill": fill} for s, n, fill in r["free"]],
        "seconds": round(time.time() - t0, 1),
    }
    from . import filetable
    for mt in r["master_tables"]:
        if mt["self_reference"]:
            path, kinds = filetable.export(rom, int(mt["address"], 16), mt["entries"], set(r["veneers"]))
            mt["export"] = path.name
            mt["kinds"] = dict(kinds.most_common())
    rom.write_json("scan.json", summary)
    rom.write_json("function_seeds.json", {f"0x{k + 0x08000000:08X}": v for k, v in r["function_seeds"].items()})
    return r, summary


def cmd_sigs(rom, args):
    matches, inferred = sigs_mod.match(rom.data, args.db)
    with open(rom.workspace / "sig_matches.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "object", "address", "size", "mode", "unique"])
        for n, obj, off, size, thumb, unique in sorted(matches, key=lambda m: m[2]):
            w.writerow([n, obj, f"0x{off + 0x08000000:08X}", size, "thumb" if thumb else "arm", unique])
    rom.write_json("sig_inferred_labels.json", {k: f"0x{v:08X}" for k, v in sorted(inferred.items())})
    by_obj = {}
    for n, obj, *_ , unique in matches:
        if unique:
            by_obj[obj] = by_obj.get(obj, 0) + 1
    return matches, inferred, by_obj


def main(argv=None):
    ap = argparse.ArgumentParser(prog="gbax", description="GBA ROM extraction toolkit")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("identify", "scan", "sigs", "extract", "palettes", "ghidra", "all"):
        p = sub.add_parser(c)
        p.add_argument("rom")
        p.add_argument("--deep", action="store_true", help="scan: test every aligned offset for compression")
        p.add_argument("--db", nargs="*", help="sigs: signature databases to use (default: all)")
        p.add_argument("--analyze", action="store_true", help="ghidra: run auto-analysis (slow)")
        p.add_argument("--rebuild", action="store_true", help="ghidra: re-import from scratch")
    for c, h in (("refs", "find pointers to and BL calls to each ADDRESS"),
                 ("decompile", "print Ghidra's decompilation of the functions containing each ADDRESS"),
                 ("callers", "decompile every function that calls each ADDRESS into one file")):
        p = sub.add_parser(c, help=h)
        p.add_argument("rom")
        p.add_argument("addresses", nargs="+", type=lambda s: int(s, 0))
        p.add_argument("--range", nargs=2, type=lambda s: int(s, 0), metavar=("LO", "HI"),
                       help="callers: only call sites in [LO, HI)")
        p.add_argument("--out", help="decompile: also write the C text to this file in the workspace")
        p.add_argument("--arm", type=lambda s: int(s, 0), default=0, metavar="SIZE",
                       help="decompile: re-disassemble SIZE bytes at the address as ARM code first")
    t = sub.add_parser("trace", help="log file loads and decoders live from mGBA's GDB server")
    t.add_argument("rom")
    t.add_argument("--launch", action="store_true", help="start mGBA with its GDB server on this ROM")
    t.add_argument("--seconds", type=float, help="stop after this many seconds (default: until the game exits)")
    t.add_argument("--port", type=int, default=2345)
    b = sub.add_parser("sigs-build", help="build a signature DB from a decomp ELF + map + ROM")
    b.add_argument("elf")
    b.add_argument("map")
    b.add_argument("built_rom")
    b.add_argument("name")
    b.add_argument("--all", action="store_true", help="include game code, not just SDK/library objects")
    args = ap.parse_args(argv)

    if args.cmd == "sigs-build":
        path, n = sigs_mod.build(args.elf, args.map, args.built_rom, args.name,
                                 objects=None if args.all else sigs_mod.SDK_OBJECTS)
        print(f"{n} signatures -> {path}")
        return

    rom = Rom.load(args.rom)
    if args.cmd == "trace":
        from . import trace
        out, summary = trace.run(rom, seconds=args.seconds, launch=args.launch, port=args.port)
        print(json.dumps(summary, indent=2, default=str))
        print(f"trace -> {out}")
        return
    if args.cmd == "refs":
        from . import re as re_mod
        for a in args.addresses:
            ptrs, calls = re_mod.find_refs(rom, a), re_mod.find_callers(rom, a)
            print(f"0x{a:08X}: {len(ptrs)} pointers {[hex(p) for p in ptrs[:40]]}")
            loads = [hex(l) for p in ptrs[:40] for l in re_mod.find_literal_loads(rom, p)]
            print(f"            loaded by ldr at {loads}")
            direct = [hex(c) for c, s in calls.items() if s is None]
            via = {}
            for c, s in calls.items():
                if s is not None:
                    via.setdefault(hex(s), []).append(hex(c))
            print(f"            {len(direct)} direct BL calls {direct[:30]}")
            for s, cs in via.items():
                print(f"            {len(cs)} calls through stub {s}: {cs[:30]}")
        return
    if args.cmd == "callers":
        from . import re as re_mod
        lo, hi = (args.range or [0, 0xFFFFFFFF])
        sites = [c for a in args.addresses for c in re_mod.find_callers(rom, a) if lo <= c < hi]
        seen, chunks = set(), []
        for addr, name, entry, text in re_mod.decompile(rom, sites):
            if entry in seen:
                continue
            seen.add(entry)
            chunks.append(f"// ===== {name} @ 0x{entry:08X} (calls at "
                          + ", ".join(hex(s) for s in sites if name and entry <= s < entry + 0x1000) + ")\n" + text)
        out = rom.workspace / (args.out or "callers.c")
        out.write_text("\n".join(chunks), encoding="utf-8")
        print(f"{len(sites)} call sites in {len(seen)} functions -> {out}")
        return
    if args.cmd == "decompile":
        from . import re as re_mod
        chunks = []
        for addr, name, entry, text in re_mod.decompile(rom, args.addresses, arm_size=args.arm):
            head = f"// ===== 0x{addr:08X} in {name} @ 0x{entry:08X}" if name else f"// ===== 0x{addr:08X}"
            chunks.append(head + "\n" + text)
        out = "\n".join(chunks)
        print(out)
        if args.out:
            (rom.workspace / args.out).write_text(out, encoding="utf-8")
        return
    print(f"{rom.path.name}: {rom.title} [{rom.code}] {rom.size // 1024} KB -> {rom.workspace}")
    if args.cmd in ("identify", "all"):
        print(json.dumps(cmd_identify(rom, args), indent=2))
    scan_r = None
    if args.cmd in ("scan", "extract", "palettes", "ghidra", "all"):
        scan_r, summary = cmd_scan(rom, args)
        print("scan:", json.dumps({k: v for k, v in summary.items() if k != "free_space_runs"}, indent=2))
    matches, inferred = [], {}
    if args.cmd in ("sigs", "ghidra", "all"):
        matches, inferred, by_obj = cmd_sigs(rom, args)
        print(f"sigs: {sum(1 for m in matches if m[5])} unique matches by object {by_obj}; "
              f"{len(inferred)} data labels inferred")
    if args.cmd in ("extract", "all"):
        out, n, made = extract_mod.extract(rom, scan_r["blobs"])
        print(f"extract: {n} BIOS-format blobs -> {out} ({made} PNG previews)")
        from . import profiles
        codec = profiles.codec_for(rom)
        for mt in scan_r["master_tables"]:
            if codec and mt.get("export"):
                out, counts = extract_mod.extract_filetable(rom, rom.workspace / mt["export"], codec)
                print(f"extract: master table {mt['address']} with the {codec.__name__.split('.')[-1]} codec "
                      f"-> {out} {counts}")
    if args.cmd in ("palettes", "all"):
        from . import palette_sources, palettes as pal_mod
        graphics, pals, ev = palette_sources.from_pointer_rom(rom, scan_r)
        files_dir = rom.workspace / "files"
        if (files_dir / "index.csv").exists():
            fg, fp, emb = palette_sources.from_file_table(rom, files_dir)
            graphics += fg
            pals += fp
            ev["embedded"] = emb
        matches = pal_mod.match_all(graphics, pals, **ev)
        matched = {m.graphic.addr for m in matches}
        out = pal_mod.write_results(rom, matches, [g for g in graphics if g.addr not in matched])
        from collections import Counter
        print(f"palettes: {len(matches)}/{len(graphics)} graphics matched "
              f"{dict(Counter(m.evidence for m in matches))} -> {out}\\index.html")
        from . import profiles
        codec = profiles.codec_for(rom)
        if codec and hasattr(codec.Decoder, "extract_sprites") and (files_dir / "index.csv").exists():
            n, sp = codec.Decoder(rom).extract_sprites(files_dir)
            print(f"palettes: {n} sprites decoded with the game's own routine -> {sp}\\index.html")
    if args.cmd in ("ghidra", "all"):
        from . import ghidra as ghidra_mod
        gpr, stats = ghidra_mod.build(rom, scan_r, matches, inferred, analyze=args.analyze, rebuild=args.rebuild)
        print(f"ghidra: {gpr}")
        for k, v in stats.items():
            print(f"  {k}: {v:,}")


if __name__ == "__main__":
    sys.exit(main())
