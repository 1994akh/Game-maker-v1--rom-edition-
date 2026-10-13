"""Build a Ghidra project for Unbound with every name we can recover applied.

Names come from:
  - vanilla FireRed v1.0 (the pokefirered ELF built in WSL): functions in the right ARM/Thumb mode, data and RAM
    labels. Symbols that symdiff.py found overwritten are skipped, since their bytes now belong to something else.
  - CFRU/DPE hook stubs and routine pointers: the new routine each one jumps to gets its CFRU/DPE name.
  - moved_symbols.py: vanilla tables/functions that Unbound relocated get their name at the new address.

Project: ghidra/Unbound.gpr (open it with apps/ghidra_*/ghidraRun.bat). Also writes reports/ghidra_labels.csv
(every recovered name in Unbound's new code/data) and, after analysis, reports/ghidra_functions.csv.

Usage: python tools/build_ghidra_project.py [--rebuild] [--analyze]
"""
import argparse
import bisect
import csv
import struct
import time
from collections import Counter

import env
import symdiff as sd

GHIDRA_DIR = env.ROOT / "ghidra"
PROJECT = PROGRAM = "Unbound"
ELF = env.ROOT / "build" / "pokefirered_v10.elf"
LANGUAGE = "ARM:LE:32:v4t"

GBA_MEMORY = [  # name, start, size, permissions
    ("BIOS", 0x00000000, 0x4000, "rx"),
    ("EWRAM", 0x02000000, 0x40000, "rwx"),
    ("IWRAM", 0x03000000, 0x8000, "rwx"),
    ("IO", 0x04000000, 0x400, "rw"),
    ("PALETTE", 0x05000000, 0x400, "rw"),
    ("VRAM", 0x06000000, 0x18000, "rw"),
    ("OAM", 0x07000000, 0x400, "rw"),
]


# ---------------------------------------------------------------- inputs

def read_elf(path):
    """Return (symbols, mode_at) from the vanilla ELF. symbols: [(name, addr, size, type)] with the Thumb bit cleared;
    mode_at(addr) gives 't', 'a' or 'd' from the ARM mapping symbols."""
    from elftools.elf.elffile import ELFFile
    raw, maps = [], []
    with open(path, "rb") as f:
        elf = ELFFile(f)
        for s in elf.get_section_by_name(".symtab").iter_symbols():
            name, val = s.name, s["st_value"]
            if name.startswith(("$t", "$a", "$d")):
                maps.append((val, name[1]))
            elif name and s["st_info"]["type"] in ("STT_FUNC", "STT_OBJECT", "STT_NOTYPE"):
                raw.append((name, val, s["st_size"], s["st_info"]["type"]))
    maps.sort()
    starts = [m[0] for m in maps]

    def mode_at(addr):
        i = bisect.bisect_right(starts, addr) - 1
        return maps[i][1] if i >= 0 else "d"

    # The Thumb bit is set on functions and on labels inside Thumb code; clear it to get the real address.
    syms = [(n, v & ~1 if (v & 1 and (t == "STT_FUNC" or mode_at(v & ~1) == "t")) else v, z, t, v & 1)
            for n, v, z, t in raw]
    arm_ranges = [(a, maps[i + 1][0] if i + 1 < len(maps) else a + 4) for i, (a, m) in enumerate(maps)
                  if m == "a" and 0x08000000 <= a < 0x0A000000]
    return syms, mode_at, arm_ranges


def read_symdiff_status():
    with open(env.REPORTS / "symbol_diff.csv", encoding="utf-8") as f:
        return {(r["name"], int(r["v10_addr"], 16)): r["status"] for r in csv.DictReader(f)}


def read_moved():
    path = env.REPORTS / "moved_symbols.csv"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [(r["name"], r["kind"], int(r["new_addr"], 16)) for r in csv.DictReader(f)]


def recover_patch_targets(hack):
    """Follow CFRU/DPE hooks and routine pointers in the hack. Returns [(source, kind, name, site, target, thumb)]."""
    out = []
    for proj, root in (("CFRU", env.EXTERNAL / "Complete-Fire-Red-Upgrade"), ("DPE", env.EXTERNAL / "DPE-Unbound")):
        for start, _, src, kind, name in sd.load_patch_lists({proj: root}):
            off = start - 0x08000000
            if not 0 <= off < len(hack) - 12:
                continue
            if kind == "hook":
                # CFRU's inserter writes: ldr rX,[pc,#0|#4]; bx rX; (2-byte pad if unaligned); .word routine|1
                if (hack[off + 1] & 0xF8) != 0x48 or hack[off + 3] != 0x47:
                    out.append((src, "hook (not applied)", name, start, None, True))
                    continue
                word = struct.unpack_from("<I", hack, off + (4 if start % 4 == 0 else 6))[0]
            elif kind in ("routine pointer", "repoint"):
                if start % 4:
                    continue
                word = struct.unpack_from("<I", hack, off)[0]
            else:
                continue
            if 0x08000000 <= word < 0x0A000000:
                out.append((src, kind, name, start, word & ~1, bool(word & 1) or kind != "repoint"))
            else:
                out.append((src, kind + " (not applied)", name, start, None, True))
    return out


# ---------------------------------------------------------------- Ghidra

def import_rom(project, monitor):
    import pyghidra
    from ghidra.app.util.opinion import BinaryLoader
    with pyghidra.program_loader().project(project).source(str(env.UNBOUND)).name(PROGRAM) \
            .loaders(BinaryLoader.class_).language(LANGUAGE).compiler("default").load() as results:
        program = results.getPrimaryDomainObject()
        with pyghidra.transaction(program, "Rebase to GBA ROM"):
            program.setImageBase(program.getAddressFactory().getDefaultAddressSpace().getAddress(0x08000000), True)
        results.save(monitor)


def annotate(program, monitor):
    import pyghidra
    from java.math import BigInteger
    from ghidra.program.flatapi import FlatProgramAPI
    from ghidra.program.model.symbol import SourceType

    flat = FlatProgramAPI(program, monitor)
    space = program.getAddressFactory().getDefaultAddressSpace()
    A = space.getAddress
    mem, st, ctx = program.getMemory(), program.getSymbolTable(), program.getProgramContext()
    tmode = ctx.getRegister("TMode")
    hack = env.UNBOUND.read_bytes()
    stats = Counter()
    labels_out = []

    def set_mode(start, end, thumb):
        ctx.setValue(tmode, A(start), A(end - 1), BigInteger.ONE if thumb else BigInteger.ZERO)

    def make_function(addr, name, size, thumb, ns=None):
        # CPU mode is set for the whole ROM up front (see below); disassembly follows it.
        a = A(addr)
        if program.getListing().getInstructionAt(a) is None:
            flat.disassemble(a)
        fn = flat.getFunctionAt(a) or flat.createFunction(a, name)
        if fn is None:
            st.createLabel(a, name, ns, SourceType.IMPORTED) if ns else flat.createLabel(a, name, True)
            return False
        fn.setName(name, SourceType.IMPORTED)
        if ns:
            fn.setParentNamespace(ns)
        return True

    def make_label(addr, name, ns=None):
        st.createLabel(A(addr), name, ns, SourceType.IMPORTED) if ns else flat.createLabel(A(addr), name, True)

    with pyghidra.transaction(program, "GBA memory map and vanilla names"):
        rom = mem.getBlock(A(0x08000000))
        rom.setName("ROM")
        rom.setWrite(False)
        rom.setExecute(True)
        for name, start, size, perms in GBA_MEMORY:
            if mem.getBlock(A(start)) is None:
                b = mem.createUninitializedBlock(name, A(start), size, False)
                b.setRead("r" in perms)
                b.setWrite("w" in perms)
                b.setExecute("x" in perms)
                b.setVolatile(name == "IO")

        status = read_symdiff_status()
        syms, mode_at, arm_ranges = read_elf(ELF)
        # GBA games are almost entirely Thumb: default the whole ROM to Thumb, then mark vanilla ARM ranges.
        set_mode(0x08000000, 0x08000000 + len(hack), True)
        for start, end in arm_ranges:
            set_mode(start, end, False)
        stats["ARM ranges"] = len(arm_ranges)
        t0 = time.time()
        for name, addr, size, typ, _ in syms:
            if 0x02000000 <= addr < 0x04000000:
                make_label(addr, name)
                stats["vanilla RAM labels"] += 1
                continue
            if not 0x08000000 <= addr < 0x09000000:
                continue
            st_ = status.get((name, addr))
            if st_ == "overwritten":
                stats["vanilla skipped (overwritten)"] += 1
                continue
            mode = mode_at(addr)
            if typ == "STT_FUNC" or (typ == "STT_NOTYPE" and size > 0 and mode in "ta"):
                ok = make_function(addr, name, size, mode != "a")
                stats["vanilla functions" if ok else "vanilla function labels"] += 1
            else:
                make_label(addr, name)
                stats["vanilla data labels"] += 1
        stats["seconds applying vanilla names"] = int(time.time() - t0)

    with pyghidra.transaction(program, "CFRU/DPE and relocated names"):
        namespaces = {}

        def ns_for(src):
            if src not in namespaces:
                namespaces[src] = st.getOrCreateNameSpace(program.getGlobalNamespace(), src, SourceType.IMPORTED)
            return namespaces[src]

        for src, kind, name, site, target, thumb in recover_patch_targets(hack):
            if target is None:
                stats[f"{src} {kind}"] += 1
                continue
            if kind == "repoint":
                make_label(target, name, ns_for(src))
            else:
                make_function(target, name, 2, thumb, ns_for(src))
                flat.setPreComment(A(site), f"{src} {kind} -> {name} @ 0x{target:08X}")
            stats[f"{src} {kind} targets named"] += 1
            labels_out.append((src, kind, name, site, target))

        for name, kind, new in read_moved():
            if kind == "code":
                make_function(new, name, 2, True, ns_for("Unbound"))
            else:
                make_label(new, name, ns_for("Unbound"))
            stats["relocated vanilla symbols named"] += 1
            labels_out.append(("Unbound", f"relocated {kind}", name, None, new))

        flat.addEntryPoint(A(0x08000000))
        flat.disassemble(A(0x08000000))

    with open(env.REPORTS / "ghidra_labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "kind", "name", "site", "address"])
        for src, kind, name, site, target in sorted(labels_out, key=lambda r: r[4]):
            w.writerow([src, kind, name, f"0x{site:08X}" if site else "", f"0x{target:08X}"])
    return stats


def export_functions(program):
    rows = []
    for fn in program.getFunctionManager().getFunctions(True):
        entry = fn.getEntryPoint().getOffset()
        ns = fn.getParentNamespace().getName()
        rows.append((fn.getName(), "" if ns == "Global" else ns, entry, fn.getBody().getNumAddresses(),
                     "new" if entry >= 0x09000000 or entry >= 0x0871A29C else "vanilla region"))
    with open(env.REPORTS / "ghidra_functions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "namespace", "entry", "size", "region"])
        for r in rows:
            w.writerow([r[0], r[1], f"0x{r[2]:08X}", r[3], r[4]])
    c = Counter((r[4], "unnamed" if r[0].startswith("FUN_") else "named") for r in rows)
    return len(rows), c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true", help="delete and re-import the program")
    ap.add_argument("--analyze", action="store_true", help="run Ghidra auto-analysis afterwards (slow)")
    args = ap.parse_args()
    if not ELF.exists():
        raise SystemExit(f"Missing {ELF}; run tools/wsl_setup.sh first.")

    import pyghidra
    pyghidra.start()
    monitor = pyghidra.task_monitor()
    GHIDRA_DIR.mkdir(exist_ok=True)
    project = pyghidra.open_project(str(GHIDRA_DIR), PROJECT, create=True)
    try:
        data = project.getProjectData()
        df = data.getFile("/" + PROGRAM)
        if df is not None and args.rebuild:
            df.delete()
            df = None
        fresh = df is None
        if fresh:
            print("importing ROM...")
            import_rom(project, monitor)
        with pyghidra.program_context(project, "/" + PROGRAM) as program:
            if fresh:
                print("applying names...")
                for k, v in annotate(program, monitor).items():
                    print(f"  {k}: {v:,}")
                program.save("Applied vanilla, CFRU/DPE and relocated names", monitor)
            if args.analyze:
                t0 = time.time()
                print("running auto-analysis...")
                pyghidra.analyze(program, monitor)
                program.save("Auto-analysis", monitor)
                print(f"  analysis took {int(time.time() - t0)}s")
            total, c = export_functions(program)
            print(f"functions: {total:,}")
            for k, v in sorted(c.items()):
                print(f"  {k[0]}, {k[1]}: {v:,}")
    finally:
        project.close()


if __name__ == "__main__":
    main()
