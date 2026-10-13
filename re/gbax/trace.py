"""Live tracing of a running game in mGBA: which files it loads, from where, and which code decodes them.

`gbax trace ROM [--launch] [--seconds N]` connects to mGBA's GDB server (or launches mGBA with it), puts a breakpoint
on the game's file loader, and logs every load. For files in formats gbax can't decode yet, it sets read watchpoints
on the file's bytes: the code that reads them next is the decoder, even if it runs from a RAM copy. Its registers
and surrounding code are saved for offline analysis (the code bytes too when it's in RAM).

Output: games/<rom>/trace/<time>/events.jsonl, summary.json and code_*.bin dumps.
"""
import csv
import json
import shutil
import subprocess
import time
from collections import Counter
from pathlib import Path

from .gdb import Gdb, GdbError
from .rom import ROM_BASE

# The Qt app first: on Windows the SDL build fails to open the GDB socket ("Debugger: Couldn't open socket").
MGBA = [Path(r"C:\Program Files\mGBA\mGBA.exe"), Path(r"C:\Program Files\mGBA\mgba-sdl.exe")]
WATCH_OFFSETS = (0, 8, 64)


def golden_sun_hooks(rom):
    """GetFile's entry is the instruction that loads the master table's address (verified for GS1: 0x08002F40)."""
    from . import re as re_mod
    scan = rom.read_json("scan.json") or {}
    tables = [m for m in scan.get("master_table_candidates", []) if m.get("self_reference")]
    if not tables:
        raise SystemExit("run `gbax scan` first: no master file table recorded")
    table = int(tables[0]["address"], 16)
    loads = [l for p in re_mod.find_refs(rom, table) if p != table + 4 for l in re_mod.find_literal_loads(rom, p)]
    if not loads:
        raise SystemExit("couldn't find the code that loads the master table")
    kinds = {}
    files_csv = rom.workspace / "files" / "index.csv"
    if files_csv.exists():
        with open(files_csv, encoding="utf-8") as f:
            for x in csv.DictReader(f):
                kinds[int(x["index"])] = (x["status"], x["first_byte_kind"])
    return {"getfile": loads[0], "table": table, "kinds": kinds}


def launch_mgba(rom_path):
    exe = next((p for p in MGBA if p.exists()), None) or shutil.which("mgba-sdl") or shutil.which("mGBA")
    if not exe:
        raise SystemExit("mGBA not found")
    return subprocess.Popen([str(exe), "-g", str(rom_path)])


def run(rom, seconds=None, launch=False, port=2345, max_events=200000):
    hooks = golden_sun_hooks(rom)
    out = rom.workspace / "trace" / time.strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True)
    proc = launch_mgba(rom.path) if launch else None
    g = Gdb(port=port)
    events = open(out / "events.jsonl", "w", encoding="utf-8")
    loads, readers = Counter(), {}
    watched = {}  # watch address -> file index
    t_end = time.time() + seconds if seconds else None
    print(f"connected; GetFile at 0x{hooks['getfile']:08X}; logging to {out}")
    try:
        g.breakpoint(hooks["getfile"])
        n = 0
        while n < max_events:
            remaining = None if t_end is None else max(0.1, t_end - time.time())
            try:
                stop = g.cont(timeout=remaining)
            except (TimeoutError, OSError):
                g.interrupt()
                break
            except GdbError:  # mGBA was closed: end the trace normally
                break
            try:
                regs, cpsr = g.registers()
            except (GdbError, OSError):
                break
            pc = regs[15]
            if pc & ~1 == hooks["getfile"] & ~1:
                idx = regs[0]
                caller = (regs[14] & ~1) - 4
                status, kind = hooks["kinds"].get(idx, ("?", "?"))
                loads[idx] += 1
                ev = {"t": round(time.time(), 3), "event": "getfile", "file": idx, "caller": f"0x{caller:08X}",
                      "status": status, "kind": kind}
                if loads[idx] == 1 and status == "raw" and kind not in ("code module (export stubs)",):
                    faddr = int.from_bytes(g.read(hooks["table"] + 4 * idx, 4), "little")
                    for off in WATCH_OFFSETS:
                        try:
                            g.watch(faddr + off, 4, "read")
                            watched[faddr + off] = idx
                        except GdbError:
                            pass
                    ev["watching"] = f"0x{faddr:08X}"
                events.write(json.dumps(ev) + "\n")
            else:
                # A watchpoint fired: someone read a watched file. Find which one from the stop reply.
                hit = None
                for part in stop.split(";"):
                    if "watch:" in part:
                        hit = int(part.split(":")[1], 16)
                if hit is None or hit not in watched:
                    hit = next(iter(watched), None)
                idx = watched.pop(hit, None) if hit is not None else None
                if hit is not None:
                    try:
                        g.clear_watch(hit, 4, "read")
                    except GdbError:
                        pass
                thumb = bool(cpsr & 0x20) if cpsr is not None else None
                ev = {"t": round(time.time(), 3), "event": "read", "file": idx,
                      "address": f"0x{hit:08X}" if hit else None, "pc": f"0x{pc:08X}",
                      "lr": f"0x{regs[14]:08X}", "thumb": thumb, "r0_r3": [f"0x{v:08X}" for v in regs[:4]]}
                if pc < ROM_BASE:  # code running from RAM: save it, it isn't in the ROM at this address
                    base = (pc & ~0x3FF) - 0x400
                    try:
                        (out / f"code_{base:08X}.bin").write_bytes(g.read(base, 0xC00))
                        ev["code_dump"] = f"code_{base:08X}.bin"
                    except GdbError:
                        pass
                readers.setdefault(idx, []).append(ev["pc"])
                events.write(json.dumps(ev) + "\n")
            events.flush()
            n += 1
            if pc & ~1 == hooks["getfile"] & ~1:
                g.step()  # step off the breakpoint before resuming
    finally:
        events.close()
        summary = {"files_loaded": len(loads), "loads": sum(loads.values()),
                   "by_kind": Counter(hooks["kinds"].get(i, ("?", "?"))[1] for i in loads),
                   "readers": {str(k): sorted(set(v)) for k, v in readers.items()}}
        (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        g.detach()
        if proc:
            proc.terminate()
    return out, summary
