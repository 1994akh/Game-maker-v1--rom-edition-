"""Measure Golden Sun 1 field movement live in mGBA (GDB stub), with scripted input.

Usage (from C:\\Users\\aaron\\Documents\\UnboundHack):
    .venv\\Scripts\\python.exe tools\\gs_movement\\measure_walk.py [--rom GS1.gba] [--sav GS1.sav] [--out DIR]

What it does
  1. Copies the ROM and its in-game .sav into a fresh work folder (the originals are only read).
  2. Launches mGBA (Qt) with its GDB server (-g) on the copy and connects (gbax.gdb).
  3. Drives the joypad by breaking right after the game's only KEYINPUT read (GS1 0x080036D6
     `ldrh r2,[r3]` with r3 = 0x04000130) and overwriting r2 with the wanted (active-low) key state.
  4. Boot: taps A / Start until one of the field controllers runs (GS1 0x0800EBEC town/dungeon,
     0x0800F2F8 world map, 0x0800F7F4 climbing); r0 at that breakpoint is the player's object.
  5. Measure: walks in 8 directions, without and with B (run), each followed by an idle gap and the
     opposite direction (to come back), and logs the player object every frame to walk_log.csv.
  6. Kills mGBA and writes walk_summary.json (speeds, frames to full speed, stop behaviour).

Player object fields used (GS1, 0x70-byte objects; see notes\\gs_movement.md):
  +0x04 u16 controller tick, +0x06 u16 facing angle (0x10000 = 360 deg, 0 = east, 0x4000 = south),
  +0x08/+0x0C/+0x10 s32 x / y(height) / z in 16.16 fixed point (pixels), +0x14 floor height,
  +0x24/+0x28/+0x2C velocity, +0x30 max speed, +0x34 acceleration, +0x38..+0x40 destination.
"""
import argparse
import csv
import json
import shutil
import statistics
import struct
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from gbax.gdb import Gdb, GdbError  # noqa: E402

MGBA = Path(r"C:\Program Files\mGBA\mGBA.exe")
GS1_DIR = ROOT / "games" / "AGSE-5c469520-Golden-Sun-USA-Europe" / "rom"
KEY_BREAK = 0x080036D8          # first instruction after `ldrh r2,[r3]` (r3 = KEYINPUT)
CONTROLLERS = {0x0800EBEC: "field", 0x0800F2F8: "worldmap", 0x0800F7F4: "climb"}
KEYS = dict(A=0x001, B=0x002, SELECT=0x004, START=0x008, RIGHT=0x010, LEFT=0x020, UP=0x040, DOWN=0x080)
DIRS = [("E", "RIGHT"), ("SE", "DOWN+RIGHT"), ("S", "DOWN"), ("SW", "DOWN+LEFT"),
        ("W", "LEFT"), ("NW", "UP+LEFT"), ("N", "UP"), ("NE", "UP+RIGHT")]
OPP = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}


def mask(names):
    m = 0
    for n in filter(None, names.split("+")):
        m |= KEYS[n]
    return m


class Session:
    def __init__(self, g):
        self.g = g

    def fast(self, data, expect_ok=False):
        """Send one packet without the 20 ms drain that Gdb.cmd does; fall back to Gdb.cmd on a bad reply."""
        self.g._send(data)
        r = self.g._recv(5)
        if expect_ok and r != "OK":
            r = self.g.cmd(data)
        return r

    def set_reg(self, n, value):
        r = self.fast(f"P{n:x}={struct.pack('<I', value & 0xFFFFFFFF).hex()}", expect_ok=True)
        if r != "OK":
            raise GdbError(f"register write refused: {r!r}")

    def read(self, addr, n):
        r = self.fast(f"m{addr:x},{n:x}")
        if len(r) != 2 * n:
            return self.g.read(addr, n)
        return bytes.fromhex(r)

    def pc_r0(self):
        regs, _ = self.g.registers()
        return regs[15], regs[0]


def run(rom_src, sav_src, out_dir, boot_frames=9000, seg=40, gap=12):
    out_dir.mkdir(parents=True, exist_ok=True)
    work = out_dir / "work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    rom = work / "gs1.gba"
    shutil.copyfile(rom_src, rom)
    if sav_src and Path(sav_src).exists():
        shutil.copyfile(sav_src, work / "gs1.sav")
    proc = subprocess.Popen([str(MGBA), "-g", str(rom)])
    rows, info = [], {"boot": None}
    try:
        g = Gdb(connect_timeout=30)
        s = Session(g)
        g.breakpoint(KEY_BREAK)
        for a in CONTROLLERS:
            g.breakpoint(a)
        player, kind, frame = None, None, 0
        # ---- boot: tap A/Start until a field controller runs
        while player is None and frame < boot_frames:
            stop = g.cont(timeout=20)
            pc, r0 = s.pc_r0()
            if pc in CONTROLLERS:
                player, kind = r0, CONTROLLERS[pc]
                break
            phase = frame % 40
            want = 0
            if phase < 3:
                want = KEYS["START"] if (frame // 40) % 3 == 0 else KEYS["A"]
            s.set_reg(2, 0x3FF & ~want)
            frame += 1
        if player is None:
            raise SystemExit(f"no field controller after {frame} frames")
        info["boot"] = dict(frames=frame, player_object=f"0x{player:08X}", controller=kind)
        for a in CONTROLLERS:
            g.clear_breakpoint(a)
        # ---- script: settle, tap B to close anything opened by the boot taps, then the walk pattern
        script = [("settle", "", 60), ("cancel", "B", 3), ("settle", "", 30), ("cancel", "B", 3), ("settle", "", 60)]
        for run_b in (False, True):
            for name, keys in DIRS:
                k = keys + ("+B" if run_b else "")
                back = "+".join(OPP[p] for p in keys.split("+")) + ("+B" if run_b else "")
                tag = ("run_" if run_b else "walk_") + name
                script += [(tag, k, seg), (tag + "_stop", "", gap), (tag + "_back", back, seg), (tag + "_rest", "", gap)]
        prev = None
        for label, keys, n in script:
            for i in range(n):
                g.cont(timeout=20)
                o = s.read(player, 0x70)
                tick, facing = struct.unpack_from("<HH", o, 4)
                x, y, z, floor = struct.unpack_from("<4i", o, 8)
                vx, vy, vz, vmax, acc, dx, dy, dz = struct.unpack_from("<8i", o, 0x24)
                ctr = struct.unpack_from("<I", s.read(0x03001800, 4))[0]
                row = dict(frame=ctr, label=label, i=i, keys=keys or "-", tick=tick, facing=f"0x{facing:04X}",
                           x=x / 65536, y=y / 65536, z=z / 65536, floor=floor / 65536,
                           vx=vx / 65536, vy=vy / 65536, vz=vz / 65536, vmax=vmax / 65536, accel=acc / 65536,
                           dest_x="" if dx == -0x80000000 else dx / 65536,
                           dest_z="" if dz == -0x80000000 else dz / 65536,
                           layer=o[0x22], raw=o.hex())
                if prev is not None:
                    row["dpos"] = ((row["x"] - prev["x"]) ** 2 + (row["z"] - prev["z"]) ** 2) ** 0.5
                rows.append(row)
                prev = row
                s.set_reg(2, 0x3FF & ~mask(keys))
        g.clear_breakpoint(KEY_BREAK)
        try:
            g.detach()
        except Exception:
            pass
    finally:
        proc.terminate()
        try:
            proc.wait(10)
        except subprocess.TimeoutExpired:
            proc.kill()
        time.sleep(1)
        shutil.rmtree(work, ignore_errors=True)  # don't leave a ROM copy behind
    with open(out_dir / "walk_log.csv", "w", newline="", encoding="utf-8") as f:
        cols = list(rows[0].keys()) + ["dpos"] if rows else []
        w = csv.DictWriter(f, fieldnames=list(dict.fromkeys(cols)))
        w.writeheader()
        w.writerows(rows)
    info["segments"] = summarize(rows)
    (out_dir / "walk_summary.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    return info


def summarize(rows):
    """Per walking segment: steady speed (px/frame), per-axis speed, frames to reach 95 % of it, blocked frames.
    The input set on frame i takes effect on the row logged at i+1 (the row is read before the input is set)."""
    out = {}
    labels = list(dict.fromkeys(r["label"] for r in rows))
    for lab in labels:
        seg = [r for r in rows if r["label"] == lab]
        if lab.endswith(("_stop", "_rest")) or lab in ("settle", "cancel"):
            moving = [round(r.get("dpos", 0), 4) for r in seg[:4]]
            out[lab] = dict(first_frames_dpos=moving)
            continue
        d = [r.get("dpos", 0) for r in seg[1:]]
        ax = [abs(seg[i + 1]["x"] - seg[i]["x"]) for i in range(len(seg) - 1)]
        az = [abs(seg[i + 1]["z"] - seg[i]["z"]) for i in range(len(seg) - 1)]
        if not d:
            continue
        steady = statistics.median(d[len(d) // 2:])
        to95 = next((i + 1 for i, v in enumerate(d) if steady and v >= 0.95 * steady), None)
        out[lab] = dict(steady_px_per_frame=round(steady, 4), steady_dx=round(statistics.median(ax[len(ax) // 2:]), 4),
                        steady_dz=round(statistics.median(az[len(az) // 2:]), 4), frames_to_95pct=to95,
                        first_frames_dpos=[round(v, 4) for v in d[:8]], zero_frames=sum(1 for v in d if v == 0),
                        vmax=seg[-1]["vmax"], accel=seg[-1]["accel"], start=(seg[0]["x"], seg[0]["z"]),
                        end=(seg[-1]["x"], seg[-1]["z"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rom", default=str(GS1_DIR / "Golden Sun (USA, Europe).gba"))
    ap.add_argument("--sav", default=str(GS1_DIR / "Golden Sun (USA, Europe).sav"))
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "out"))
    ap.add_argument("--seg", type=int, default=40, help="frames per walking segment")
    a = ap.parse_args()
    info = run(Path(a.rom), Path(a.sav), Path(a.out), seg=a.seg)
    print(json.dumps(info["boot"]))
    for k, v in info["segments"].items():
        if "steady_px_per_frame" in v:
            print(f"{k:16s} {v['steady_px_per_frame']:.4f} px/f  dx {v['steady_dx']:.4f} dz {v['steady_dz']:.4f} "
                  f"to95 {v['frames_to_95pct']}  zero {v['zero_frames']}  first {v['first_frames_dpos'][:6]}")


if __name__ == "__main__":
    main()
