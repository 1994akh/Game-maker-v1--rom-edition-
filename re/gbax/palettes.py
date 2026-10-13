"""Match graphics to palettes and render them in colour.

Evidence, strongest first:
  parallel   a graphics array and a palette array of the same length (struct stride 4..64), paired by index
  struct     a pointer to the palette sits within a few words of a pointer to the graphic (same struct or literal pool)
  adjacent   the palette is stored near the graphic in the ROM (assets from one source file are linked together)
  embedded   the palette is at the start of the same file (custom-format games)
Every candidate also gets a content score: with the right palette, neighbouring pixels have similar colours relative
to the palette's overall spread; a wrong palette turns the same index pattern into high-contrast noise. The score
breaks ties and picks the palette bank (and, when unknown, 4bpp vs 8bpp).
"""
import bisect
import csv
from dataclasses import dataclass, field

import numpy as np
from PIL import Image

EVIDENCE_BONUS = {"parallel": 0.6, "struct": 0.35, "embedded": 0.3, "adjacent": 0.0}
MAX_TILES = 256  # tiles used for scoring; enough to judge, keeps big tilesets fast


@dataclass
class Graphic:
    addr: int                  # where it lives (ROM address of the blob or file)
    data: bytes                # decoded tile data
    bpps: tuple = (4,)         # bit depths to consider
    label: str = ""


@dataclass
class Palette:
    addr: int
    colors: np.ndarray         # (n, 3) uint8 RGB
    raw: bytes = b""
    label: str = ""

    @property
    def banks(self):
        return len(self.colors) // 16


@dataclass
class Match:
    graphic: Graphic
    palette: Palette
    bank: int
    bpp: int
    evidence: str
    score: float
    alternatives: list = field(default_factory=list)


# ---------------------------------------------------------------- colour helpers

def bgr555(raw):
    w = np.frombuffer(raw[: len(raw) & ~1], dtype="<u2").astype(np.uint16)
    rgb = np.stack([(w & 31), (w >> 5) & 31, (w >> 10) & 31], -1).astype(np.uint16)
    return ((rgb << 3) | (rgb >> 2)).astype(np.uint8)


def palette_like(raw, n=16):
    """n BGR555 colours with the unused top bit clear, not all the same."""
    if len(raw) < 2 * n:
        return False
    w = np.frombuffer(raw[: 2 * n], dtype="<u2")
    return bool((w & 0x8000).sum() == 0 and len(np.unique(w)) >= 3)


def palette_like_strict(raw, n=16):
    """palette_like, minus the data that commonly imitates it: pointer tables (high halves 0x02xx/0x03xx/0x08xx/0x09xx),
    small-integer tables (map layouts, IDs) and near-monochrome runs."""
    if not palette_like(raw, n):
        return False
    w = np.frombuffer(raw[: 2 * n], dtype="<u2")
    hi = w[1::2] >> 8
    if np.isin(hi, (0x02, 0x03, 0x08, 0x09)).mean() >= 0.25:
        return False
    if (w < 0x0100).mean() >= 0.4 or (w < 0x0400).mean() >= 0.75:
        return False
    b = np.frombuffer(raw[: 2 * n], dtype=np.uint8)
    if ((b >= 0x20) & (b < 0x7F)).mean() >= 0.9:  # ASCII text
        return False
    if (np.diff(w.astype(np.int32)) > 0).mean() >= 0.9:  # steadily increasing numbers (order/ID tables)
        return False
    g, b = (w >> 5) & 31, (w >> 10) & 31
    if ((g > 2) | (b > 2)).sum() < 3:
        return False
    return len(np.unique(w)) >= 5


def tile_indices(data, bpp, tiles_wide=16, max_tiles=None):
    tb = 32 if bpp == 4 else 64
    n = len(data) // tb
    if max_tiles:
        n = min(n, max_tiles)
    if n == 0:
        return None
    raw = np.frombuffer(data[: n * tb], dtype=np.uint8)
    if bpp == 4:
        px = np.empty(raw.size * 2, dtype=np.uint8)
        px[0::2], px[1::2] = raw & 0x0F, raw >> 4
    else:
        px = raw.copy()
    tiles = px.reshape(n, 8, 8)
    rows = (n + tiles_wide - 1) // tiles_wide
    pad = rows * tiles_wide - n
    if pad:
        tiles = np.concatenate([tiles, np.zeros((pad, 8, 8), np.uint8)])
    return tiles.reshape(rows, tiles_wide, 8, 8).transpose(0, 2, 1, 3).reshape(rows * 8, tiles_wide * 8)


def fit_score(idx, colors):
    """Lower is better: mean neighbour colour difference / mean spread of the colours actually used."""
    if idx.max() >= len(colors):
        return float("inf")
    c = colors[idx].astype(np.float32)
    # Within-tile neighbours only (tile seams are arbitrary in a raw tile dump).
    h = np.abs(c[:, 1:] - c[:, :-1]).sum(-1)
    v = np.abs(c[1:] - c[:-1]).sum(-1)
    h = h[:, (np.arange(h.shape[1]) % 8) != 7]
    v = v[(np.arange(v.shape[0]) % 8) != 7]
    tv = (h.mean() + v.mean()) / 2
    used = np.unique(idx)
    used = used[used != 0] if len(used) > 2 else used  # colour 0 is usually transparent
    if len(used) < 2:
        return float("inf")
    uc = colors[used].astype(np.float32)
    spread = np.abs(uc[:, None, :] - uc[None, :, :]).sum(-1).mean()
    if spread < 24:  # near-uniform palettes would trivially score well
        return float("inf")
    return float(tv / spread)


def auto_width(data, bpp):
    """Sprite-sized data (whole 64x64 frames) reads best 8 tiles wide; everything else 16."""
    n = len(data) // (32 if bpp == 4 else 64)
    return 8 if n and n % 64 == 0 and n <= 512 else 16


def guess_bitmap_width(px, candidates=range(16, 257, 8)):
    """Width of a linear 8bpp bitmap: at the true width a pixel usually equals the one directly below it.
    Widths that are a fraction of the truth also line up, so prefer the widest width scoring near the best.
    Very narrow widths match trivially, so widths start at 16 and the image must be at least 16 rows tall."""
    px = np.asarray(px, dtype=np.uint8)
    scores = {}
    for w in candidates:
        if len(px) < 16 * w:
            continue
        scores[w] = float((px[w:] != px[:-w]).mean())
    if not scores:
        return 32
    best = min(scores.values())
    return max(w for w, s in scores.items() if s <= best * 1.15 + 0.01)


def render(data, bpp, colors, tiles_wide=None):
    idx = tile_indices(data, bpp, tiles_wide or auto_width(data, bpp))
    if idx is None:
        return None
    if idx.max() >= len(colors):
        colors = np.concatenate([colors, np.zeros((256 - len(colors), 3), np.uint8)])
    return Image.fromarray(colors[idx], mode="RGB")


# ---------------------------------------------------------------- evidence

def strided_arrays(ptr_offs, gaps=range(4, 68, 4), min_len=8):
    """Arrays of pointers at a constant stride: [(start, stride, count)]. Overlapping/embedded runs are skipped."""
    s = set(int(o) for o in ptr_offs)
    out = []
    for g in gaps:
        seen = set()
        for o in sorted(s):
            if o in seen or (o - g) in s:
                continue
            n, p = 0, o
            while p in s:
                seen.add(p)
                n += 1
                p += g
            if n >= min_len:
                out.append((o, g, n))
    return out


def array_pairs(arrays, target_at, is_graphic, is_palette):
    """Pair graphics arrays with palette arrays. Returns (fields, parallel), each {graphic: {palette: 1}}.

    fields:   both are fields of one array of structs (same stride, starts less than a stride apart). Each graphic
              is paired with the palette field of its own struct, so neighbouring structs can't be confused.
    parallel: separate tables of exactly the same length (e.g. a picture table and a palette table), paired by index;
              among several equal-length palette tables the nearest wins.
    """
    def kind(t):
        g, p = is_graphic(t), is_palette(t)
        return "a" if g and p else "g" if g else "p" if p else "o"

    # Split runs wherever the kind of target changes: tables stored back to back (FireRed's back pics, palettes and
    # shiny palettes) merge into one pointer run, and a run can also pick up an unrelated pointer just before or
    # after a table, which would shift every index-based pairing. Ambiguous entries ("a": data that could be either)
    # take the kind of the segment they're in.
    segs = []
    for start, stride, n in arrays:
        tg = [target_at(start + i * stride) for i in range(n)]
        ks = [kind(t) for t in tg]
        i = 0
        while i < n:
            if ks[i] == "o":
                i += 1
                continue
            j, cur = i, ks[i]
            while j < n and (ks[j] == cur or ks[j] == "a" or cur == "a"):
                if cur == "a" and ks[j] in "gp":
                    cur = ks[j]
                j += 1
                if j < n and ks[j] not in (cur, "a") and cur != "a":
                    break
            if cur == "a":
                cur = "p"  # a column of nothing but ambiguous entries is multi-bank palettes far more often than tiles
            if j - i >= 8:
                pure = all(k == cur for k in ks[i:j])
                segs.append((start + i * stride, stride, j - i, cur, tg[i:j], pure))
            i = j
    # Drop every-other-entry samples of a denser segment of the same kind, but only when that denser segment is
    # uniform: a struct table that is pointers end to end forms a dense run mixing columns, and it mustn't swallow
    # the real per-field columns.
    by_kind = {}
    for s in segs:
        if s[5]:
            by_kind.setdefault(s[3], []).append(s)
    kept = []
    for s in segs:
        st, sd, n, k, _, _ = s
        end = st + sd * (n - 1)
        if not any(o[1] < sd and sd % o[1] == 0 and (st - o[0]) % o[1] == 0 and o[0] <= st
                   and o[0] + o[1] * (o[2] - 1) >= end for o in by_kind.get(k, ())):
            kept.append(s)
    gfx_arrays = [(st, sd, n, tg, pure) for st, sd, n, k, tg, pure in kept if k == "g"]
    pal_arrays = [(st, sd, n, tg, pure) for st, sd, n, k, tg, pure in kept if k == "p"]
    array_pairs.palette_columns = {t for pa in pal_arrays for t in pa[3]}
    fields, parallel = {}, {}
    for gs, gstride, gn, gt, gpure in gfx_arrays:
        same_struct = [pa for pa in pal_arrays if pa[1] == gstride and 0 < abs(pa[0] - gs) < gstride]
        if same_struct:
            delta = min(same_struct, key=lambda pa: abs(pa[0] - gs))[0] - gs
            for k, t in enumerate(gt):
                pt = target_at(gs + k * gstride + delta)
                if is_graphic(t) and is_palette(pt) and pt != t:
                    fields.setdefault(t, {})[pt] = 1
            continue
        # Separate parallel tables: only clean, uniform tables of the same stride and exact length qualify.
        if not gpure or gn < 16:
            continue
        equal = [pa for pa in pal_arrays if pa[2] == gn and pa[1] == gstride and pa[4]]
        if not equal:
            continue
        best = min(equal, key=lambda pa: abs(pa[0] - gs))
        for t, pt in zip(gt, best[3]):
            if is_graphic(t) and is_palette(pt) and pt != t:
                parallel.setdefault(t, {})[pt] = 1
    return fields, parallel


def struct_pairs(ptr_offs, target_at, is_graphic, is_palette):
    """A palette pointer in the word right after a graphic pointer: {graphic: {palette: times seen together}}.

    Measured on FireRed, the +4 position is right 80% of the time and every other offset 4-40%; when +4 and address
    adjacency disagree, +4 was right 60 times out of 63. So only +4 counts."""
    pairs = {}
    for o in ptr_offs:
        o = int(o)
        t = target_at(o)
        if not is_graphic(t):
            continue
        pt = target_at(o + 4)
        if pt is not None and pt != t and is_palette(pt):
            d = pairs.setdefault(t, {})
            d[pt] = d.get(pt, 0) + 1
    return pairs


# ---------------------------------------------------------------- matching

# Precision of each kind of evidence used alone, measured on FireRed v1.0 against symbol names
# (tools/eval_palettes.py): parallel (strict) 100%, fields 95%, palette pointer at +4 80% (but right 60/63 times
# when it disagrees with adjacency), next palette after the graphic 81%, nearest palette before 58%.
EVIDENCE_RANK = {"parallel": 0, "fields": 1, "struct": 2, "embedded": 3, "adjacent": 4, "adjacent-before": 5}
WEAK_EVIDENCE = {"embedded", "adjacent", "adjacent-before"}
NOISE_FIT = 0.5


def best_bank(g, pal):
    """Best (fit, bank, bpp) for one palette: content fit only chooses the bank and the bit depth."""
    best = None
    for bpp in g.bpps:
        if bpp == 8 and len(pal.colors) < 256:
            continue
        idx = tile_indices(g.data, bpp, max_tiles=MAX_TILES)
        if idx is None:
            continue
        for b in ([0] if bpp == 8 else range(pal.banks)):
            cols = pal.colors if bpp == 8 else pal.colors[b * 16:(b + 1) * 16]
            s = fit_score(idx, cols)
            if best is None or s < best[0]:
                best = (s, b, bpp)
    return best


def match_all(graphics, palettes, struct=None, parallel=None, embedded=None, fields=None, neighbours=4,
              window=0x10000):
    """Match every graphic. Candidates are ranked by evidence (parallel > struct > embedded > adjacent), then by how
    often the pairing was seen, then by address distance (a palette stored just after the graphic first); the
    content fit only picks the bank/bit depth, and rejects a candidate that can't display the graphic at all."""
    pal_by_addr = {p.addr: p for p in palettes}
    pal_addrs = sorted(pal_by_addr)
    matches = []
    for g in graphics:
        cands = {}
        for ev, src in (("fields", fields), ("parallel", parallel), ("struct", struct), ("embedded", embedded)):
            found = (src or {}).get(g.addr, ())
            for pa in found:
                if pa in pal_by_addr and pa not in cands:
                    seen = found[pa] if isinstance(found, dict) else 1
                    cands[pa] = (EVIDENCE_RANK[ev], -seen, abs(pa - g.addr), ev)
        cands.pop(g.addr, None)
        i = bisect.bisect_right(pal_addrs, g.addr)
        for pa in pal_addrs[i:i + neighbours]:  # palettes stored after the graphic, nearest first
            if pa - g.addr <= window and pa not in cands:
                cands[pa] = (EVIDENCE_RANK["adjacent"], 0, pa - g.addr, "adjacent")
        for pa in pal_addrs[max(0, i - neighbours):i]:
            if g.addr - pa <= window and pa not in cands and pa != g.addr:
                cands[pa] = (EVIDENCE_RANK["adjacent-before"], 0, g.addr - pa, "adjacent-before")
        for pa, key in sorted(cands.items(), key=lambda kv: kv[1][:3]):
            fit = best_bank(g, pal_by_addr[pa])
            if fit is None or fit[0] == float("inf"):
                continue
            # The fit can't rank palettes, but it does separate plausible renderings (FireRed/Unbound median 0.2)
            # from noise (0.6+). Weak evidence that renders as noise is rejected.
            if key[3] in WEAK_EVIDENCE and fit[0] > NOISE_FIT:
                continue
            alts = [f"0x{a:08X}" for a, _ in sorted(cands.items(), key=lambda kv: kv[1][:3]) if a != pa][:3]
            matches.append(Match(g, pal_by_addr[pa], fit[1], fit[2], key[3], fit[0], alts))
            break
    return matches


GALLERY_CSS = """
:root { --bg: #f6f6f4; --fg: #1d1d1b; --muted: #6b6b66; --card: #ffffff; --line: #deded8; }
@media (prefers-color-scheme: dark) { :root { --bg: #161615; --fg: #ececea; --muted: #9a9a94; --card: #22221f;
  --line: #34342f; } }
body { margin: 0; padding: 16px; background: var(--bg); color: var(--fg); font: 14px/1.4 system-ui, sans-serif; }
h1 { font-size: 18px; margin: 0 0 4px; } p { color: var(--muted); margin: 0 0 16px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }
figure { margin: 0; background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 8px; }
img { width: 100%; image-rendering: pixelated; background: repeating-conic-gradient(#0001 0 25%, #0000 0 50%) 0/16px 16px; }
figcaption { font-size: 12px; color: var(--muted); word-break: break-all; margin-top: 6px; }
.ev { display: inline-block; padding: 0 6px; border-radius: 4px; border: 1px solid var(--line); }
"""


def write_gallery(out, title, rows):
    cards = "\n".join(
        f'<figure><img loading="lazy" src="{r[8]}" alt=""><figcaption>{r[0]} {r[1]}<br>'
        f'palette {r[2]} bank {r[4]}, {r[5]}bpp <span class="ev">{r[6]}</span></figcaption></figure>'
        for r in rows if r[8])
    (out / "index.html").write_text(
        f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{title}</title><style>{GALLERY_CSS}</style><h1>{title}</h1>"
        f"<p>{len(rows)} graphics matched to palettes by gbax. Evidence tag shows how each match was made.</p>"
        f"<div class=grid>{cards}</div>", encoding="utf-8")


def write_results(rom, matches, unmatched, out_name="color"):
    out = rom.workspace / out_name
    out.mkdir(exist_ok=True)
    for old in out.glob("*.png"):  # previews from earlier runs that may no longer match
        old.unlink()
    rows = []
    for m in matches:
        cols = m.palette.colors if m.bpp == 8 else m.palette.colors[m.bank * 16:(m.bank + 1) * 16]
        img = render(m.graphic.data, m.bpp, cols)
        name = f"{m.graphic.addr:08X}.png"
        if img is not None:
            img.save(out / name)
        else:
            name = ""
        rows.append((f"0x{m.graphic.addr:08X}", m.graphic.label, f"0x{m.palette.addr:08X}", m.palette.label, m.bank,
                     m.bpp, m.evidence, round(m.score, 3), name, m.alternatives))
    write_gallery(out, f"{rom.title} [{rom.code}] graphics", rows)
    with open(out / "palettes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["graphic", "graphic_label", "palette", "palette_label", "bank", "bpp", "evidence", "fit", "png",
                    "alternatives"])
        w.writerows(rows)
        for g in unmatched:
            w.writerow([f"0x{g.addr:08X}", g.label, "", "", "", "", "unmatched", "", "", ""])
    return out
