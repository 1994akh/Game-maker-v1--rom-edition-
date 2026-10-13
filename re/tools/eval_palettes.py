"""Measure gbax palette matching against ground truth from the FireRed v1.0 symbols.

A graphic and its palette are a correct pair when their symbol names share a stem once words like Pic/Gfx/Tiles/
Palette/Shiny are removed (gMonFrontPic_Bulbasaur <-> gMonPalette_Bulbasaur, gItemIcon_Potion <-> gItemIconPalette_Potion).

Usage: python tools/eval_palettes.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gbax import palette_sources, palettes, scan  # noqa: E402
from gbax.rom import Rom  # noqa: E402

import env  # noqa: E402

WORDS = ["palettes", "palette", "frontpic", "backpic", "pics", "pic", "gfx", "tilemap", "tiles", "tile", "shiny",
         "pals", "pal",
         "sheet", "image", "img", "normal", "_lz", "lz"]


def stem(name):
    s = re.sub(r"^[gs](?=[A-Z])", "", name).lower()
    for w in WORDS:
        s = s.replace(w, "")
    return re.sub(r"_+", "_", s).strip("_")


def main():
    rom = Rom.load(env.ROOT / "build" / "pokefirered_v10.gba")
    names = {}
    for line in Path(env.SYMBOLS_V10).read_text().splitlines():
        p = line.split()
        if len(p) == 4 and p[0].startswith("08"):
            names.setdefault(int(p[0], 16), p[3])
    r = scan.scan(rom)
    graphics, pals, ev = palette_sources.from_pointer_rom(rom, r)
    print(f"{len(graphics)} graphics, {len(pals)} palette candidates; evidence: "
          + ", ".join(f"{k} {len(v)}" for k, v in ev.items()))
    matches = palettes.match_all(graphics, pals, **ev)
    pal_stems = Counter(stem(names[p.addr]) for p in pals if p.addr in names)
    by_ev, total, correct, has_truth = Counter(), Counter(), 0, 0
    wrong_examples = []
    for m in matches:
        g, p = names.get(m.graphic.addr), names.get(m.palette.addr)
        if not g or stem(g) not in pal_stems:
            continue
        has_truth += 1
        total[m.evidence] += 1
        if p and stem(p) == stem(g):
            correct += 1
            by_ev[m.evidence] += 1
        elif len(wrong_examples) < 8:
            wrong_examples.append((g, p, m.evidence, round(m.score, 2)))
    truth_graphics = sum(1 for g in graphics if names.get(g.addr) and stem(names[g.addr]) in pal_stems)
    print(f"matched {len(matches)}/{len(graphics)} graphics")
    print(f"graphics with a known correct palette: {truth_graphics}; matched {has_truth}; correct {correct} "
          f"({correct / max(has_truth, 1):.0%})")
    for ev in total:
        print(f"  {ev}: {by_ev[ev]}/{total[ev]} correct")
    for w in wrong_examples:
        print("  wrong:", w)


if __name__ == "__main__":
    main()
