"""Draw Halcyra's proposed world map as a clean schematic, from scratch (shapes and labels only).

Nothing here comes from game art: every coast is a smoothed polygon built from the layout numbers below.
The same numbers are written to world-layout.json, and the script prints the main sailing distances.

Usage:  python draw_world_map.py            (writes world-map.png and world-layout.json beside this file)

World units are Golden Sun world-map pixels on a proposed 8,192 x 8,192 canvas (512 x 512 cells of 16 px).
North is up. Bearings are degrees clockwise from north, measured from the Pinnacle at the centre.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "C:/Windows/Fonts"
SS = 2  # supersampling factor
W, H = 1600, 1100
C = 4096.0
SHIP_PX_S = 75.0  # sailing speed today (speed_scale 1.25 at 60 fps)
RUN_PX_S = 45.0   # running on the world map today (speed_scale 0.5)


def font(size, bold=False, italic=False):
    name = "segoeuib.ttf" if bold else ("segoeuii.ttf" if italic else "segoeui.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), int(size * SS))


# ---------------------------------------------------------------- layout numbers

def polar(bearing, r):
    t = math.radians(bearing)
    return (C + r * math.sin(t), C - r * math.cos(t))


def angdiff(a, b):
    d = (a - b + 180) % 360 - 180
    return d


def radius_table(table, smooth=6):
    """Periodic radius function from {bearing: radius}, linearly resampled per degree then smoothed."""
    keys = sorted(table)
    per = []
    for deg in range(360):
        # find neighbours
        lo = max([k for k in keys if k <= deg], default=keys[-1] - 360)
        hi = min([k for k in keys if k > deg], default=keys[0] + 360)
        rlo = table[lo % 360] if lo >= 0 else table[lo + 360]
        rhi = table[hi % 360]
        f = (deg - lo) / (hi - lo)
        per.append(rlo + (rhi - rlo) * f)
    out = []
    for deg in range(360):
        s = sum(per[(deg + k) % 360] for k in range(-smooth, smooth + 1))
        out.append(s / (2 * smooth + 1))
    return lambda b: out[int(round(b)) % 360]


MERIDIA_R = radius_table({
    0: 1250, 15: 1200, 30: 1100, 45: 1000, 60: 1000, 75: 1050, 90: 1100, 100: 1080, 105: 1030, 115: 1090,
    130: 1120, 145: 1150, 160: 1200, 175: 1280, 190: 1250, 205: 1150, 220: 1050, 235: 1000, 250: 1050,
    265: 1120, 275: 1130, 290: 1080, 305: 1000, 320: 980, 335: 1080, 350: 1180})


def gale_in(b):
    return 1950 + 30 * math.sin(math.radians(3 * b))


def gale_out(b):
    return 2400 + 40 * math.sin(math.radians(5 * b + 20))


BITE_AT, BITE_DEPTH, BITE_WIDTH = 92.0, 1150.0, 16.0


def rim(b):
    return 3800 + 40 * math.sin(math.radians(6 * b)) - BITE_DEPTH * math.exp(-(angdiff(b, BITE_AT) / BITE_WIDTH) ** 2)


FALLS_W = 150

MARROW = polar(62, 1600)
# Marrow Isle's outline, relative to its centre (world px), clockwise from the north.
MARROW_SHAPE = [(-60, -205), (40, -215), (140, -190), (215, -140), (255, -60), (262, 20), (250, 90), (238, 125),
                (262, 150), (290, 182), (262, 205), (222, 180), (195, 155), (155, 150), (125, 172), (110, 212),
                (60, 222), (-40, 215), (-140, 195), (-220, 150), (-265, 70), (-275, -20), (-250, -100),
                (-200, -160), (-130, -195)]
MARROW_REEF = [(262, -55), (300, -48)], [(338, -30), (352, 40), (348, 120), (322, 185), (292, 200)]
MARROW_FEATURES = {
    "stonehollow": (40, 40), "vault": (10, -60), "vault_hill": (0, -95), "cove": (172, 168), "beacon": (284, 182),
    "sea_caves": (258, 8), "berth": (20, -212), "north_caves": (-130, -190), "quarry": (-195, 70),
    "lake1": (-115, -45), "lake2": (-205, -25), "rockslide": (-85, 48), "tortell": (318, 105),
    "reef_gap": (318, -42), "holdfast": (215, 262), "west_gate": (-25, 40)}


def mx(rel):
    return (MARROW[0] + rel[0], MARROW[1] + rel[1])


# Places: id, name, (x, y) world, kind, stars, note.
# kinds: act1 (open in Act I), act1c (seen in Act I, closed until later), rumour (? on the Chart in the demo),
#        act2 (Act II or later), sinks (sinks at the Breaking), risen (rises at the Breaking), landmark, lost (fallen rim town)
PLACES = []


def place(pid, name, xy, kind, stars="", note=""):
    PLACES.append({"id": pid, "name": name, "x": round(xy[0]), "y": round(xy[1]), "kind": kind,
                   "stars": stars, "note": note})
    return xy


CANALPORT = place("canalport", "Canalport", polar(100, 1075), "act1", "1", "Harbour front on Saltmarsh Reach")
REACH = place("saltmarsh_reach", "Saltmarsh Reach", polar(103, 1260), "act1", "1", "Tidal bay of mudbanks and channels")
ELDERGROVE = place("eldergrove", "The Eldergrove", polar(272, 1120), "act1", "2", "Village and river landing")
EMBRAL = place("embral", "Embral Isle", polar(186, 1700), "act1c", "2", "Crew 2 only in Act I; blockaded")
LANTERN = place("lantern_reef", "Lantern Reef", polar(318, 1700), "act1", "2", "Inside the north fog; pilot gate")
BASTION = place("bastion_rock", "Bastion Rock", polar(256, 1650), "act1c", "2", "Crew 2 only; sea-gate shut")
place("marrow_isle", "Marrow Isle", MARROW, "act1", "1", "Home")
HUSH = place("hushwater", "Hushwater", polar(22, 1650), "rumour", "1", "Island of the week, after the demo")
TWIN = place("twin_bells", "Twin Bells", polar(148, 1620), "rumour", "2", "Island of the week, after the demo")
TORTELL = place("tortell", "Tortell's isle", mx(MARROW_FEATURES["tortell"]), "act1c", "1", "Inside Marrow's reef; from m10")
COCKLE = place("cockle_cay", "Cockle Cay", polar(88, 1520), "sinks", "1", "Wild islet, open from m4; sinks at the Breaking")
SANDMERE = place("sandmere", "Sandmere", polar(222, 1600), "sinks", "1", "Wild islet; sinks at the Breaking")
DRIFT = place("driftholm", "Driftholm", polar(345, 1600), "sinks", "2", "Wild islet; sinks at the Breaking")
SHELFBACK = place("shelfback", "Shelfback", polar(205, 1800), "risen", "2", "Risen isle, south-west of Embral")
BELLSTONE = place("bellstone", "Bellstone", polar(40, 1500), "risen", "3", "Risen isle")
FARERSTEP = place("farers_step", "Farer's Step", polar(125, 1560), "risen", "4", "Risen isle")
CHURN = place("churn", "The Churn", polar(166, 1780), "act2", "3", "Whirlpool and sea grotto (Whirlpool)")
RELAY = place("galeway_relay", "Galeway relay (the eye)", polar(78, 2175), "act2", "5", "Blown at m11; airship only after")
SKYSPOUT = place("skyspout", "Skyspout", polar(28, 2175), "act2", "4", "Dead updraft, m17")
FALLHAVEN = place("fallhaven", "Fallhaven", polar(92, rim(92) - 90), "act1", "", "Crew 2 (m2), both crews (m9); ruin after")
BAZAAR = place("bazaar", "Tradewind Bazaar", polar(62, 3050), "act1", "2", "Crew 2 (m8); Act II port")
IRONFIST = place("ironfist", "Ironfist Arena", polar(114, 3050), "act2", "3", "m15; the Glimmer Saucer")
CLOCKWORK = place("clockwork_key", "Clockwork Key", polar(132, 3300), "act2", "3", "Tuesday Again")
SILVERDEEP = place("silverdeep", "Silverdeep", polar(150, 2950), "landmark", "4", "Whirl and lighthouse; Deep Shelf below")
CORALREACH = place("coralreach", "Coralreach", polar(182, 2900), "act2", "3", "Pearlhollow below (m16)")
KELPWOOD = place("kelpwood", "Kelpwood wreck", polar(165, 3350), "act2", "4", "Salvage and Dive")
LEVIATHAN = place("leviathan", "Leviathan Shoal", polar(208, 3250), "act2", "4", "A Stillwater")
GLOAM = place("gloam_shore", "Gloam Shore", polar(268, 3050), "act2", "4", "m20; maelstrom")
UMBRAL = place("umbral_gate", "Umbral Gate", polar(298, rim(298) - 40), "landmark", "5", "Black falls, north-west rim")
THUNDER = place("thunderhead", "Thunderhead Atoll", polar(336, 3150), "act2", "4", "The Sentinel")
STORMSPIRE = place("stormspire", "Stormspire", polar(0, 2750), "landmark", "5", "Top above the Cloudreach (m19)")
COURT = place("lighthouse_court", "Lighthouse-court", polar(22, 3100), "act2", "4", "m13; the four warriors")
TANARRA = place("tanarra", "Speakers' isle", polar(40, 3350), "act2", "3", "The Speakers of Tanarra")
HIDDEN1 = place("gloam_hidden_1", "hidden isle", polar(250, 3350), "act2", "4", "Fog sight (m20)")
HIDDEN2 = place("gloam_hidden_2", "hidden isle", polar(284, 3420), "act2", "4", "Fog sight (m20)")
for pid, nm, b in [("gullstone", "Gullstone", 74), ("saltcombe", "Saltcombe", 82), ("hales_point", "Hale's Point", 102),
                   ("kettle_bay", "Kettle Bay", 110)]:
    place(pid, nm, polar(b, rim(b) - 45), "lost", "", "Lost rim town")
PINNACLE = place("pinnacle", "The Pinnacle", (C, C), "landmark", "4", "Closed until Act III")
CROWN_LANDING = place("crown_landing", "Crown Landing", (C + 260, C - 20), "act2", "4", "River port under the Pinnacle; boom shut")
RANCH = place("doduo_ranch", "Doduo ranch", (C + 560, C - 330), "act2", "2", "The Dodo Derby")
COAST_POST = place("coast_post", "coast post", polar(268, 1150), "act1", "", "Tidewarden customs at the Eldwater's mouth")

CLOUD_RECT = (5000 - 1408, 1550 - 1408, 5000 + 1408, 1550 + 1408)
SHELF_RECT = (4850 - 1408, 6650 - 1408, 4850 + 1408, 6650 + 1408)
FOG_BLOBS = [(polar(318, 1700), 330), (polar(305, 1680), 260), (polar(330, 1760), 240), (polar(295, 1700), 200)]

ROUTES = {
    "marrow_canalport": [mx((200, 210)), (5700, 3800), (5560, 4180), (5430, 4330), (5300, 4300), CANALPORT],
    "canalport_eldergrove_south": [CANALPORT, (5430, 4330), (5350, 4850), (4950, 5250), (4400, 5500), (3900, 5480),
                                   (3400, 5300), (3150, 5000), (2850, 4500), (2850, 4100), ELDERGROVE],
    "marrow_eldergrove_north": [mx((200, 210)), (5420, 3640), (5130, 3520), (5050, 3150), (4800, 2800),
                                (4300, 2650), (3800, 2680), (3420, 3000), (3200, 3350), (2950, 3700), (2850, 4000),
                                ELDERGROVE],
    "eldergrove_lantern": [ELDERGROVE, (2850, 3900), (2850, 3400), (2960, 3050), (2990, 2890)],
    "marrow_lantern": [mx((200, 210)), (5420, 3640), (5130, 3520), (5050, 3150), (4800, 2800), (4300, 2650),
                       (3800, 2680), (3420, 3000), (3100, 2950), (2990, 2890)],
    "marrow_tortell": [mx((200, 210)), mx((300, 230)), mx((380, 120)), mx((380, -60)), mx((318, -42)),
                       mx((290, 20)), TORTELL],
    "bazaar_fallhaven": [BAZAAR, (6850, 3400), (6720, 4000), FALLHAVEN],
    "marrow_fallhaven_act2": [mx((300, 230)), RELAY, (6560, 4100), FALLHAVEN],
}
WALKS = {
    "m12_dustplain_home": [(3990, 5330), (4250, 4950), (4700, 4550), (5140, 4250), (4900, 3550)],
    "stonehollow_quarry": [mx(MARROW_FEATURES["west_gate"]), mx(MARROW_FEATURES["quarry"])],
}


def length(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


# ---------------------------------------------------------------- drawing helpers

class Panel:
    def __init__(self, x0, y0, x1, y1, ox, oy, ow, oh):
        self.vx0, self.vy0, self.vx1, self.vy1 = x0, y0, x1, y1
        self.ox, self.oy, self.ow, self.oh = ox, oy, ow, oh
        self.s = min(ow / (x1 - x0), oh / (y1 - y0))
        # centre the view in the box
        self.cx = (ow - (x1 - x0) * self.s) / 2
        self.cy = (oh - (y1 - y0) * self.s) / 2
        self.img = Image.new("RGBA", (ow * SS, oh * SS), "#17202b")
        self.d = ImageDraw.Draw(self.img)

    def p(self, xy):
        return ((xy[0] - self.vx0) * self.s * SS + self.cx * SS, (xy[1] - self.vy0) * self.s * SS + self.cy * SS)

    def ring(self, rfun, step=1):
        return [self.p(polar(b, rfun(b))) for b in range(0, 360, step)]

    def poly(self, pts, fill, outline=None, width=1):
        self.d.polygon(pts, fill=fill, outline=outline, width=int(width * SS) if outline else 0)

    def line(self, pts, fill, width=1):
        self.d.line(pts, fill=fill, width=max(1, int(width * SS)), joint="curve")

    def dashed(self, pts, fill, width=1, dash=8, gap=6):
        dash *= SS
        gap *= SS
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            seg = math.dist((x0, y0), (x1, y1))
            if seg == 0:
                continue
            t = 0.0
            while t < seg:
                t2 = min(seg, t + dash)
                a = (x0 + (x1 - x0) * t / seg, y0 + (y1 - y0) * t / seg)
                b = (x0 + (x1 - x0) * t2 / seg, y0 + (y1 - y0) * t2 / seg)
                self.d.line([a, b], fill=fill, width=max(1, int(width * SS)))
                t = t2 + gap

    def ell(self, xy, rx, ry, fill, outline=None, width=1, world=True):
        cx, cy = self.p(xy) if world else xy
        if world:
            rx, ry = rx * self.s * SS, ry * self.s * SS
        else:
            rx, ry = rx * SS, ry * SS
        self.d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=outline,
                       width=int(width * SS) if outline else 0)

    def text(self, xy, s, size=14, bold=False, italic=False, fill="#1d2b3a", halo="#ffffff", anchor="mm",
             dx=0, dy=0, world=True, halo_w=3):
        x, y = self.p(xy) if world else (xy[0] * SS, xy[1] * SS)
        if "\n" in s and anchor[1] in "tbs":
            anchor = anchor[0] + {"t": "a", "b": "d", "s": "d"}[anchor[1]]
        self.d.text((x + dx * SS, y + dy * SS), s, font=font(size, bold, italic), fill=fill, anchor=anchor,
                    stroke_width=int(halo_w * SS) if halo else 0, stroke_fill=halo, align="center")

    def marker(self, xy, kind, size=6):
        x, y = self.p(xy)
        r = size * SS
        if kind == "act1":
            self.d.ellipse([x - r, y - r, x + r, y + r], fill="#c2410c", outline="#ffffff", width=int(1.5 * SS))
        elif kind == "act1c":
            self.d.ellipse([x - r, y - r, x + r, y + r], fill="#ffffff", outline="#c2410c", width=int(2.5 * SS))
            self.d.line([(x - r * 0.7, y + r * 0.7), (x + r * 0.7, y - r * 0.7)], fill="#c2410c", width=int(2 * SS))
        elif kind == "rumour":
            self.d.ellipse([x - r, y - r, x + r, y + r], fill="#fff7d6", outline="#a16207", width=int(2 * SS))
            self.d.text((x, y + 0.5 * SS), "?", font=font(size * 1.5, True), fill="#a16207", anchor="mm")
        elif kind == "act2":
            self.d.ellipse([x - r, y - r, x + r, y + r], fill="#5b3fa0", outline="#ffffff", width=int(1.5 * SS))
        elif kind == "sinks":
            self.d.polygon([(x - r, y - r * 0.8), (x + r, y - r * 0.8), (x, y + r)], fill="#0f766e",
                           outline="#ffffff")
        elif kind == "risen":
            self.d.polygon([(x - r, y + r * 0.8), (x + r, y + r * 0.8), (x, y - r)], fill="#b45309",
                           outline="#ffffff")
        elif kind == "landmark":
            pts = []
            for i in range(10):
                a = math.radians(-90 + i * 36)
                rr = r * 1.35 if i % 2 == 0 else r * 0.6
                pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
            self.d.polygon(pts, fill="#eab308", outline="#713f12")
        elif kind == "lost":
            self.d.line([(x - r, y - r), (x + r, y + r)], fill="#e11d48", width=int(2 * SS))
            self.d.line([(x - r, y + r), (x + r, y - r)], fill="#e11d48", width=int(2 * SS))

    def done(self):
        return self.img.convert("RGB")


def falls_ticks(pn, every=4):
    for b in range(0, 360, every):
        a = pn.p(polar(b, rim(b) + 15))
        z = pn.p(polar(b, rim(b) + FALLS_W - 15))
        pn.line([a, z], fill="#bcd7ee", width=1)


def storm_marks(pn, every=9):
    for b in range(0, 360, every):
        for k, f in enumerate((0.3, 0.65)):
            r = gale_in(b) + (gale_out(b) - gale_in(b)) * f
            a = pn.p(polar(b + k * 4, r))
            z = pn.p(polar(b + k * 4 + 4, r + 25))
            pn.line([a, z], fill="#6b7682", width=1.6)


def draw_base(pn, detail):
    # Rimfalls band, the Wide, the Galeway, the Calm
    pn.poly(pn.ring(lambda b: rim(b) + FALLS_W), fill="#f3f8fc")
    falls_ticks(pn, every=3 if detail else 4)
    pn.poly(pn.ring(rim), fill="#2e5e8e")
    pn.poly(pn.ring(gale_out), fill="#9aa4ae")
    storm_marks(pn)
    pn.poly(pn.ring(gale_in), fill="#8fd3cd")


def draw_fog(pn, alpha=150):
    over = Image.new("RGBA", pn.img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    for xy, r in FOG_BLOBS:
        cx, cy = pn.p(xy)
        rr = r * pn.s * SS
        od.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(232, 236, 240, alpha))
    pn.img.alpha_composite(over)
    pn.d = ImageDraw.Draw(pn.img)


def draw_meridia(pn, regions=True):
    coast = [pn.p(polar(b, MERIDIA_R(b))) for b in range(360)]
    pn.poly(coast, fill="#a7cf8f", outline="#4b6b3a", width=1.2)
    if not regions:
        return
    # region tints, clipped to the land with a mask
    mask = Image.new("L", pn.img.size, 0)
    ImageDraw.Draw(mask).polygon(coast, fill=255)
    tint = Image.new("RGBA", pn.img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(tint)
    big = 3000

    def rect(x0, y0, x1, y1):
        return [pn.p((x0, y0)), pn.p((x1, y0)), pn.p((x1, y1)), pn.p((x0, y1))]
    td.polygon(rect(C - big, C - big, C + big, C - 700), fill=(230, 238, 243, 255))   # Frostmarch
    td.polygon(rect(C - big, C + 760, C + big, C + big), fill=(232, 213, 150, 255))   # Dustplain
    td.polygon(rect(C - big, C - 700, C - 110, C + 760), fill=(104, 160, 96, 255))    # the Greenwild
    td.polygon(rect(C + 110, C - 700, C + big, C + 760), fill=(190, 219, 140, 255))   # Brightcoast
    clipped = Image.new("RGBA", pn.img.size, (0, 0, 0, 0))
    clipped.paste(tint, (0, 0), mask)
    pn.img.alpha_composite(clipped)
    pn.d = ImageDraw.Draw(pn.img)
    pn.poly(coast, fill=None, outline="#4b6b3a", width=1.2)
    # the Spine
    spine = [(C - 20, C - 860), (C + 15, C - 500), (C - 10, C - 150), (C + 10, C + 200), (C - 15, C + 520),
             (C + 10, C + 760)]
    pn.line([pn.p(q) for q in spine], fill="#7a5a3a", width=5 if pn.s > 0.15 else 3)
    for i in range(len(spine) - 1):
        for f in (0.25, 0.75):
            q = (spine[i][0] + (spine[i + 1][0] - spine[i][0]) * f, spine[i][1] + (spine[i + 1][1] - spine[i][1]) * f)
            x, y = pn.p(q)
            r = (9 if pn.s > 0.15 else 5) * SS
            pn.d.polygon([(x - r, y + r * 0.6), (x + r, y + r * 0.6), (x, y - r)], fill="#8a6a4a", outline="#5b4330")
    # rivers
    crown = [CROWN_LANDING, (C + 600, C + 90), CANALPORT]
    eld = [(C - 220, C - 140), (C - 700, C - 90), ELDERGROVE]
    rime = [(C - 90, C - 820), (C - 120, C - 1050), polar(354, MERIDIA_R(354) - 10)]
    for rv in (crown, eld, rime):
        pn.line([pn.p(q) for q in rv], fill="#3b82c4", width=3 if pn.s > 0.15 else 2)


def draw_marrow_small(pn):
    pts = [pn.p(mx(q)) for q in MARROW_SHAPE]
    pn.poly(pts, fill="#b5d79a", outline="#3f5f2f", width=1)


def draw_island(pn, xy, rx, ry, fill="#d8c48f", inner="#9cc58a"):
    pn.ell(xy, rx, ry, fill=fill, outline="#6b5a33", width=1)
    if rx > 60:
        pn.ell(xy, rx * 0.65, ry * 0.65, fill=inner)


def legend_item(d, x, y, kind, label, fsize=15):
    pn = None
    r = 7 * SS
    X, Y = x * SS, y * SS
    if kind in ("act1", "act1c", "rumour", "act2", "sinks", "risen", "landmark", "lost"):
        tmp = type("T", (), {})()
        # reuse Panel.marker logic on the main canvas
        fake = Panel(0, 0, 1, 1, 0, 0, 1, 1)
        fake.img, fake.d = None, d
        fake.p = lambda xy: (X, Y)
        fake.marker((0, 0), kind, size=7)
    elif kind.startswith("swatch:"):
        col = kind.split(":", 1)[1]
        d.rectangle([X - r * 1.4, Y - r, X + r * 1.4, Y + r], fill=col, outline="#334155", width=SS)
    elif kind.startswith("dash:"):
        col = kind.split(":", 1)[1]
        for k in range(3):
            d.line([(X - r * 1.6 + k * r * 1.2, Y), (X - r * 1.0 + k * r * 1.2, Y)], fill=col, width=3 * SS)
    d.text((X + 16 * SS, Y), label, font=font(fsize), fill="#1d2b3a", anchor="lm")


# ---------------------------------------------------------------- the three panels

def world_panel():
    pn = Panel(C - 4000, C - 4000, C + 4000, C + 4000, 0, 0, 800, 790)
    draw_base(pn, detail=False)
    # quarter dividers
    for b in (45, 135, 225, 315):
        pn.dashed([pn.p(polar(b, gale_out(b) + 30)), pn.p(polar(b, rim(b) - 20))], fill="#9cc3e6", width=1.5,
                  dash=7, gap=6)
    draw_fog(pn, alpha=120)
    draw_meridia(pn, regions=True)
    draw_marrow_small(pn)
    for xy, rx, ry in [(EMBRAL, 170, 150), (LANTERN, 60, 60), (BASTION, 70, 60)]:
        draw_island(pn, xy, rx, ry)
    # layer footprints
    for rect_, col, lab, lpos in [(CLOUD_RECT, "#c4b5fd", "The Cloudreach (above)", (CLOUD_RECT[0] + 60, CLOUD_RECT[1] + 140)),
                                  (SHELF_RECT, "#5eead4", "The Deep Shelf (below)", (SHELF_RECT[0] + 60, SHELF_RECT[3] - 140))]:
        x0, y0, x1, y1 = rect_
        pts = [pn.p(q) for q in [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]]
        pn.dashed(pts, fill=col, width=2.2, dash=10, gap=7)
        pn.text(lpos, lab, size=15, bold=True, fill="#ffffff", halo="#2e3a5a", anchor="lm", halo_w=3)
    # Undertow tunnel
    pn.dashed([pn.p((4300, 5300)), pn.p((4180, 4700)), pn.p((4130, 4250))], fill="#5eead4", width=2, dash=5, gap=4)
    pn.text((4330, 4780), "Undertow", size=12, fill="#ccfbf1", halo="#134e4a", anchor="lm", halo_w=2)
    # Calm inset box
    pts = [pn.p(q) for q in [(2150, 2150), (6250, 2150), (6250, 6150), (2150, 6150), (2150, 2150)]]
    pn.dashed(pts, fill="#fde68a", width=1.6, dash=6, gap=5)
    pn.text((6230, 2180), "inset", size=13, italic=True, fill="#fde68a", halo="#1e293b", anchor="ra",
            halo_w=2)
    # quarter names
    for b, nm in [(0, "NORTHREACH"), (90, "EASTWATER"), (180, "SOUTHDEEP"), (270, "WESTGLOAM")]:
        r = 3420 if b in (0, 180) else 3300
        if b == 90:
            xy = polar(70, 3400)
        else:
            xy = polar(b, r)
        pn.text(xy, nm, size=22, bold=True, fill="#e0f2fe", halo="#1e3a5f", halo_w=3)
    pn.text(polar(232, 2185), "THE GALEWAY", size=14, bold=True, fill="#1f2937", halo="#d1d5db", halo_w=2)
    pn.text(polar(318, 3930), "THE RIMFALLS", size=14, bold=True, fill="#1e3a5f", halo="#f3f8fc", halo_w=2)
    pn.text((C - 600, C + 1450), "the Calm", size=13, italic=True, fill="#0f3d3a", halo="#c8f0ea", halo_w=2)
    pn.text((C, C + 260), "MERIDIA", size=16, bold=True, fill="#1f3b16", halo="#e8f5df", halo_w=3)
    # places in the Wide and on the ring
    labels = [
        (STORMSPIRE, "Stormspire", 0, -16, "ms"), (COURT, "Lighthouse-court", 0, 16, "mt"),
        (THUNDER, "Thunderhead Atoll", 0, 16, "mt"), (TANARRA, "Speakers' isle", 10, 0, "lm"),
        (BAZAAR, "Tradewind Bazaar", 12, 0, "lm"), (FALLHAVEN, "Fallhaven", -12, 0, "rm"),
        (IRONFIST, "Ironfist Arena", 12, 0, "lm"), (CLOCKWORK, "Clockwork Key", 0, 16, "mt"),
        (SILVERDEEP, "Silverdeep", 12, 4, "lm"), (CORALREACH, "Coralreach", 0, 16, "mt"),
        (KELPWOOD, "Kelpwood wreck", 10, 0, "lm"), (LEVIATHAN, "Leviathan Shoal", 0, 16, "mt"),
        (GLOAM, "Gloam Shore", 0, 16, "mt"), (UMBRAL, "Umbral Gate", 0, 16, "mt"),
        (SKYSPOUT, "Skyspout", -10, -6, "rs"), (RELAY, "the eye", 0, -12, "ms"),
    ]
    for xy, s, dx, dy, an in labels:
        pl = next(p for p in PLACES if (p["x"], p["y"]) == (round(xy[0]), round(xy[1])))
        pn.marker(xy, pl["kind"], size=6)
        pn.text(xy, s, size=14, bold=True, fill="#ffffff", halo="#1e3a5f", anchor=an, dx=dx, dy=dy, halo_w=3)
    for p in PLACES:
        if p["kind"] == "lost":
            pn.marker((p["x"], p["y"]), "lost", size=4)
        if p["id"].startswith("gloam_hidden"):
            pn.marker((p["x"], p["y"]), "rumour", size=6)
    pn.text(polar(84, 3520), "the bite:\nlost rim towns", size=12, fill="#fecdd3", halo="#3f1d2b",
            anchor="mm", halo_w=2)
    # Farside arrow
    a, z = polar(96, rim(96) + 40), polar(100, rim(100) + 700)
    pn.line([pn.p(a), pn.p(z)], fill="#f472b6", width=2.5)
    pn.text(z, "Farside\n(postgame)", size=12, bold=True, fill="#fbcfe8", halo="#3f1d2b", anchor="mm",
            dy=2, halo_w=2)
    # small Calm labels
    pn.marker(MARROW, "act1", size=5)
    pn.marker(PINNACLE, "landmark", size=6)
    return pn.done()


def calm_panel():
    pn = Panel(2150, 2150, 6250, 6150, 0, 0, 770, 735)
    draw_base(pn, detail=True)
    draw_fog(pn, alpha=170)
    # Saltmarsh Reach shallows
    reach = [polar(96, 1060), polar(97, 1230), polar(104, 1330), polar(111, 1260), polar(111, 1080)]
    pn.poly([pn.p(q) for q in reach], fill="#c9e8d2", outline="#6aa287", width=1)
    for k in range(5):
        a, b = polar(98 + k * 3, 1110), polar(98 + k * 3, 1270)
        pn.dashed([pn.p(a), pn.p(b)], fill="#7fb59a", width=1, dash=3, gap=3)
    draw_meridia(pn, regions=True)
    # Marrow Isle with its reef
    pts = [pn.p(mx(q)) for q in MARROW_SHAPE]
    pn.poly(pts, fill="#b5d79a", outline="#3f5f2f", width=1.2)
    for seg in MARROW_REEF:
        pn.dashed([pn.p(mx(q)) for q in seg], fill="#f8fafc", width=2, dash=3, gap=3)
    # islands
    for xy, rx, ry in [(EMBRAL, 175, 150), (LANTERN, 55, 45), (BASTION, 70, 60), (HUSH, 90, 70), (TWIN, 55, 40),
                       (COCKLE, 45, 30), (SANDMERE, 50, 32), (DRIFT, 45, 35), (TORTELL, 16, 12),
                       (SHELFBACK, 60, 40), (BELLSTONE, 55, 40), (FARERSTEP, 55, 40)]:
        draw_island(pn, xy, rx, ry)
    draw_island(pn, (TWIN[0] + 85, TWIN[1] + 40), 45, 32)
    pn.dashed([pn.p((TWIN[0] + 40, TWIN[1] + 15)), pn.p((TWIN[0] + 50, TWIN[1] + 30))], fill="#d8c48f", width=3,
              dash=3, gap=2)
    # Embral volcano
    ex, ey = pn.p(EMBRAL)
    r = 22 * SS
    pn.d.polygon([(ex - r, ey + r * 0.6), (ex + r, ey + r * 0.6), (ex, ey - r)], fill="#7c2d12", outline="#431407")
    pn.d.ellipse([ex - 4 * SS, ey - r - 4 * SS, ex + 4 * SS, ey - r + 4 * SS], fill="#f97316")
    # Churn whirlpool
    cx, cy = pn.p(CHURN)
    for rr in (5, 9, 13):
        pn.d.arc([cx - rr * SS, cy - rr * SS, cx + rr * SS, cy + rr * SS], 20, 300, fill="#1e3a5f", width=2 * SS)
    # routes
    for key, col in [("marrow_canalport", "#7c2d12"), ("canalport_eldergrove_south", "#7c2d12"),
                     ("marrow_eldergrove_north", "#7c2d12"), ("eldergrove_lantern", "#7c2d12")]:
        pn.dashed([pn.p(q) for q in ROUTES[key]], fill=col, width=1.8, dash=5, gap=5)
    # m12 walk home (Act II)
    pn.dashed([pn.p(q) for q in WALKS["m12_dustplain_home"]], fill="#5b3fa0", width=2, dash=2, gap=4)
    # region names on Meridia
    pn.text((C, C - 1000), "FROSTMARCH", size=15, bold=True, fill="#334155", halo="#f1f5f9", halo_w=2)
    pn.text((C + 640, C + 270), "BRIGHTCOAST", size=15, bold=True, fill="#365314", halo="#ecfccb", halo_w=2)
    pn.text((C, C + 1020), "DUSTPLAIN", size=15, bold=True, fill="#713f12", halo="#fef3c7", halo_w=2)
    pn.text((C - 600, C + 330), "THE\nGREENWILD", size=15, bold=True, fill="#14532d", halo="#dcfce7", halo_w=2)
    pn.text((C + 70, C - 610), "the Spine", size=12, italic=True, fill="#3f2a17", halo="#f5f0e6", anchor="lm",
            halo_w=2)
    pn.marker(PINNACLE, "landmark", size=9)
    pn.text(PINNACLE, "the Pinnacle", size=13, bold=True, fill="#1f2937", halo="#ffffff", anchor="rm", dx=-14,
            halo_w=2)
    pn.marker(CROWN_LANDING, "act2", size=5)
    pn.text((C + 640, C + 70), "Crownwater", size=11, italic=True, fill="#1e40af", halo="#e0f2fe", anchor="mb",
            dy=-4, halo_w=2)
    pn.text((C - 640, C - 120), "Eldwater", size=11, italic=True, fill="#1e40af", halo="#e0f2fe", anchor="ms",
            dy=-4, halo_w=2)
    pn.marker(RANCH, "act2", size=5)
    pn.text(RANCH, "Doduo ranch", size=11, fill="#3b0764", halo="#f5f3ff", anchor="lm", dx=8, halo_w=2)
    # Act I places
    lab = [
        (CANALPORT, "act1", "Canalport", -12, 0, "rm"),
        (REACH, None, "Saltmarsh\nReach", 6, 22, "mt"),
        (ELDERGROVE, "act1", "The Eldergrove\n(river landing)", -12, 0, "rm"),
        (EMBRAL, "act1c", "Embral Isle\n(blockaded)", 0, 26, "mt"),
        (LANTERN, "act1", "Lantern Reef\n(fog: Vesper pilots)", 0, -14, "ms"),
        (BASTION, "act1c", "Bastion Rock\n(sea-gate shut)", 0, 16, "mt"),
        (HUSH, "rumour", "Hushwater", 0, 14, "mt"),
        (TWIN, "rumour", "Twin Bells", -12, 0, "rm"),
        (COCKLE, "sinks", "Cockle Cay", 10, 0, "lm"),
        (SANDMERE, "sinks", "Sandmere", -10, 0, "rm"),
        (DRIFT, "sinks", "Driftholm", 0, 14, "mt"),
        (SHELFBACK, "risen", "Shelfback", 0, 14, "mt"),
        (BELLSTONE, "risen", "Bellstone", 10, 0, "lm"),
        (FARERSTEP, "risen", "Farer's Step", 10, 0, "lm"),
        (CHURN, None, "the Churn", 16, 0, "lm"),
        (COAST_POST, None, "coast post", -10, 18, "rm"),
    ]
    for xy, kind, s, dx, dy, an in lab:
        if kind:
            pn.marker(xy, kind, size=6)
        pn.text(xy, s, size=13, bold=kind in ("act1", "act1c"), fill="#1d2b3a", halo="#ffffff", anchor=an, dx=dx,
                dy=dy, halo_w=2.5)
    pn.marker(MARROW, "act1", size=7)
    pn.text(mx((-60, -235)), "Marrow Isle (home)", size=14, bold=True, fill="#1d2b3a", halo="#ffffff", anchor="ms",
            halo_w=2.5)
    pn.marker(TORTELL, "act1c", size=4)
    # Galeway and sea labels
    pn.text(polar(135, 2090), "THE GALEWAY", size=13, bold=True, fill="#1f2937", halo="#d1d5db", halo_w=2)
    pn.text(polar(236, 2140), "storm wall", size=11, italic=True, fill="#1f2937", halo="#d1d5db", halo_w=2)
    pn.text(polar(300, 1460), "the north fog", size=12, italic=True, fill="#334155", halo="#f8fafc", halo_w=2)
    pn.text(polar(58, 2090), "to Eastwater and the rim", size=11, italic=True, fill="#1f2937", halo="#d1d5db",
            halo_w=2)
    # sailing-time tags
    t = {k: length(v) / SHIP_PX_S for k, v in ROUTES.items()}
    pn.text((5720, 3950), f"~{t['marrow_canalport']:.0f} s", size=12, bold=True, fill="#7c2d12", halo="#ffffff",
            anchor="lm", halo_w=2)
    pn.text((4400, 5560), f"~{t['canalport_eldergrove_south']:.0f} s", size=12, bold=True, fill="#7c2d12",
            halo="#ffffff", anchor="mt", halo_w=2)
    pn.text((4300, 2600), f"~{t['marrow_eldergrove_north']:.0f} s", size=12, bold=True, fill="#7c2d12",
            halo="#ffffff", anchor="ms", halo_w=2)
    pn.text((2800, 3500), f"~{t['eldergrove_lantern']:.0f} s", size=12, bold=True, fill="#7c2d12", halo="#ffffff",
            anchor="rm", halo_w=2)
    pn.text((4700, 4560), "m12 walk home", size=11, italic=True, fill="#3b0764", halo="#f5f3ff", anchor="lm",
            dx=6, halo_w=2)
    return pn.done()


def marrow_panel():
    pn = Panel(MARROW[0] - 330, MARROW[1] - 260, MARROW[0] + 420, MARROW[1] + 300, 0, 0, 470, 300)
    pn.img.paste("#8fd3cd", [0, 0, pn.img.size[0], pn.img.size[1]])
    # Galeway edge in the corner
    pn.poly(pn.ring(gale_out), fill="#9aa4ae")
    storm_marks(pn, every=3)
    pn.poly(pn.ring(gale_in), fill="#8fd3cd")
    # lagoon tint
    lag = [mx(q) for q in [(255, -60), (300, -48), (338, -30), (352, 40), (348, 120), (322, 185), (292, 200),
                           (262, 150), (238, 125), (250, 90), (262, 20)]]
    pn.poly([pn.p(q) for q in lag], fill="#b9ece6")
    pts = [pn.p(mx(q)) for q in MARROW_SHAPE]
    pn.poly(pts, fill="#b5d79a", outline="#3f5f2f", width=1.5)
    for seg in MARROW_REEF:
        pn.dashed([pn.p(mx(q)) for q in seg], fill="#475569", width=2.2, dash=3, gap=3)
    f = MARROW_FEATURES
    pn.ell(mx(f["vault_hill"]), 120, 68, fill="#c8a879", outline="#7a5a3a", width=1)
    for k in ("lake1", "lake2"):
        pn.ell(mx(f[k]), 45, 26, fill="#7cc4e8", outline="#2c6e94", width=1)
    # roads
    road = "#8b5e34"
    pn.line([pn.p(mx(f["stonehollow"])), pn.p(mx(f["vault"]))], fill=road, width=2.5)
    pn.line([pn.p(mx(f["stonehollow"])), pn.p(mx((110, 110))), pn.p(mx(f["cove"]))], fill=road, width=2.5)
    pn.dashed([pn.p(mx(f["west_gate"])), pn.p(mx((-120, 60))), pn.p(mx(f["quarry"]))], fill=road, width=2.5,
              dash=5, gap=3)
    pn.line([pn.p(mx((200, 160))), pn.p(mx((240, 150))), pn.p(mx(f["beacon"]))], fill=road, width=1.6)
    pn.dashed([pn.p(mx((240, 140))), pn.p(mx((255, 70))), pn.p(mx(f["sea_caves"]))], fill=road, width=1.6, dash=3,
              gap=3)
    # underground river and sea stair
    pn.dashed([pn.p(mx((60, -85))), pn.p(mx((150, -40))), pn.p(mx((235, 5)))], fill="#2563eb", width=2, dash=4,
              gap=3)
    pn.dashed([pn.p(mx((10, -110))), pn.p(mx((18, -200)))], fill="#7c3aed", width=2, dash=4, gap=3)
    # Stonehollow houses
    sx, sy = pn.p(mx(f["stonehollow"]))
    for ox, oy in [(-8, -4), (6, -6), (-2, 6), (12, 5)]:
        x, y = sx + ox * SS, sy + oy * SS
        pn.d.rectangle([x - 4 * SS, y - 3 * SS, x + 4 * SS, y + 4 * SS], fill="#f5f0e6", outline="#5b4330")
        pn.d.polygon([(x - 5 * SS, y - 3 * SS), (x + 5 * SS, y - 3 * SS), (x, y - 8 * SS)], fill="#b45309")
    # beacon
    bx, by = pn.p(mx(f["beacon"]))
    pn.d.ellipse([bx - 5 * SS, by - 5 * SS, bx + 5 * SS, by + 5 * SS], fill="#facc15", outline="#713f12",
                 width=SS)
    # rockslide
    rx_, ry_ = pn.p(mx(f["rockslide"]))
    for ox, oy in [(-4, 0), (3, -3), (4, 3), (-1, 4)]:
        pn.d.ellipse([rx_ + (ox - 3) * SS, ry_ + (oy - 3) * SS, rx_ + (ox + 3) * SS, ry_ + (oy + 3) * SS],
                     fill="#78716c")
    # cave mouths
    for k in ("sea_caves", "berth", "north_caves"):
        x, y = pn.p(mx(f[k]))
        pn.d.ellipse([x - 5 * SS, y - 4 * SS, x + 5 * SS, y + 4 * SS], fill="#1f2937")
    # quarry
    qx, qy = pn.p(mx(f["quarry"]))
    pn.d.rectangle([qx - 12 * SS, qy - 8 * SS, qx + 12 * SS, qy + 8 * SS], fill="#d6d3d1", outline="#57534e",
                   width=SS)
    # ship at anchor in the cove
    cx, cy = pn.p(mx(f["cove"]))
    pn.d.polygon([(cx - 7 * SS, cy), (cx + 7 * SS, cy), (cx + 4 * SS, cy + 4 * SS), (cx - 4 * SS, cy + 4 * SS)],
                 fill="#7c2d12")
    pn.d.line([(cx, cy), (cx, cy - 9 * SS)], fill="#7c2d12", width=SS)
    tx, ty = pn.p(TORTELL)
    pn.d.ellipse([tx - 7 * SS, ty - 5 * SS, tx + 7 * SS, ty + 5 * SS], fill="#d8c48f", outline="#6b5a33")
    pn.d.rectangle([tx - 3 * SS, ty - 5 * SS, tx + 3 * SS, ty], fill="#f472b6")
    T = lambda xy, s, an, dx=0, dy=0, b=False, size=11.5: pn.text(mx(xy), s, size=size, bold=b, fill="#1d2b3a",
                                                                 halo="#ffffff", anchor=an, dx=dx, dy=dy, halo_w=2)
    T(f["stonehollow"], "Stonehollow", "lm", dx=16, b=True, size=12.5)
    T(f["vault_hill"], "the Vault (in the hill)", "mm", dy=-2)
    T(f["cove"], "the cove: jetty,\nTully, Cidrick's yard", "mt", dx=-30, dy=14)
    T(f["beacon"], "beacon", "lm", dx=8)
    T(f["sea_caves"], "sea caves", "rm", dx=-8)
    T(f["berth"], "Wayfarer's cave (m10)", "lm", dx=8, dy=-2)
    T(f["north_caves"], "North Shore Caves", "ms", dy=-8)
    T(f["quarry"], "Dunstan's quarry", "mt", dy=12)
    T(f["lake1"], "lakes", "mm")
    T(f["rockslide"], "rockslide (west road)", "mb", dy=-6)
    T(f["tortell"], "Tortell", "lm", dx=9)
    T(f["reef_gap"], "reef gap", "ms", dy=-6)
    T((320, 50), "lagoon", "mm", size=10.5)
    T((-185, -110), "highlands", "mm", size=11)
    T((22, -8), "Vault road", "lm", dx=4, size=10)
    T((100, 112), "south road", "rm", dx=-4, size=10)
    pn.text((MARROW[0] - 320, MARROW[1] + 290), "Marrow Isle", size=15, bold=True, fill="#1d2b3a", halo="#ffffff",
            anchor="ld", halo_w=2.5)
    pn.text((MARROW[0] + 405, MARROW[1] - 250), "Galeway", size=11, bold=True, fill="#1f2937", halo="#d1d5db",
            anchor="ra", halo_w=2)
    return pn.done()


def main():
    img = Image.new("RGB", (W * SS, H * SS), "#f6f1e6")
    d = ImageDraw.Draw(img)
    d.text((24 * SS, 30 * SS), "Halcyra: the world map", font=font(28, True), fill="#1d2b3a", anchor="lm")
    d.text((372 * SS, 32 * SS), "proposed layout, 24 Oct. A schematic drawn from scratch. North is up.",
           font=font(16, italic=True), fill="#475569", anchor="lm")
    wp = world_panel()
    img.paste(wp, (10 * SS, 58 * SS))
    # world panel title
    d.text((22 * SS, 72 * SS), "The whole world", font=font(19, True), fill="#ffffff", anchor="lm",
           stroke_width=3 * SS, stroke_fill="#17202b")
    cp = calm_panel()
    img.paste(cp, (820 * SS, 58 * SS))
    d.text((832 * SS, 72 * SS), "The Calm and Act I", font=font(19, True), fill="#ffffff", anchor="lm",
           stroke_width=3 * SS, stroke_fill="#17202b")
    mp = marrow_panel()
    img.paste(mp, (820 * SS, 798 * SS))
    # frames
    for box in [(10, 58, 810, 848), (820, 58, 1590, 793), (820, 798, 1290, 1098)]:
        d.rectangle([b * SS for b in box], outline="#334155", width=2 * SS)
    # legend
    lx, ly = 22, 866
    d.text((lx * SS, ly * SS), "Key", font=font(18, True), fill="#1d2b3a", anchor="lm")
    items = [
        ("act1", "Act I place, open"), ("act1c", "seen in Act I, closed for now"),
        ("rumour", "rumour on the Chart (built after the demo)"), ("act2", "Act II or later"),
        ("sinks", "small isle that sinks at the Breaking"), ("risen", "isle that rises at the Breaking"),
        ("landmark", "tall landmark you steer by"), ("lost", "rim town already lost"),
        ("swatch:#8fd3cd", "the Calm (inner sea)"), ("swatch:#9aa4ae", "the Galeway (storm ring)"),
        ("swatch:#2e5e8e", "the Wide (outer sea)"), ("swatch:#f3f8fc", "the Rimfalls (world edge)"),
        ("swatch:#e8ecf0", "fog"), ("dash:#7c2d12", "first-visit sailing route, Act I"),
        ("dash:#c4b5fd", "layer footprint (own map, same grid)"), ("dash:#5b3fa0", "mission 12's walk home"),
    ]
    for i, (k, lab) in enumerate(items):
        col, row = i // 8, i % 8
        legend_item(d, lx + 12 + col * 400, ly + 26 + row * 24, k, lab, fsize=14.5)
    # notes box beside the Marrow inset
    nx, ny = 1305, 806
    d.text((nx * SS, ny * SS), "Sailing, first visit", font=font(17, True), fill="#1d2b3a", anchor="la")
    t = {k: length(v) / SHIP_PX_S for k, v in ROUTES.items()}
    rows = [
        ("Marrow Isle to Canalport", t["marrow_canalport"]),
        ("Canalport to the Eldergrove", t["canalport_eldergrove_south"]),
        ("Marrow Isle to the Eldergrove", t["marrow_eldergrove_north"]),
        ("The Eldergrove to Lantern Reef", t["eldergrove_lantern"]),
        ("Marrow Isle to Lantern Reef", t["marrow_lantern"]),
        ("Marrow Isle to Tortell (m10)", t["marrow_tortell"]),
        ("Bazaar to Fallhaven (Act II)", t["bazaar_fallhaven"]),
    ]
    for i, (lab, secs) in enumerate(rows):
        d.text(((nx) * SS, (ny + 34 + i * 25) * SS), lab, font=font(13.5), fill="#1d2b3a", anchor="la")
        d.text(((nx + 278) * SS, (ny + 34 + i * 25) * SS), f"{secs:.0f} s", font=font(13.5, True),
               fill="#7c2d12", anchor="ra")
    d.text((nx * SS, (ny + 34 + 7 * 25 + 6) * SS),
           "At today's ship speed. Places you've\nbeen: 'Sail here' from the helm.",
           font=font(12.5, italic=True), fill="#475569", anchor="la")
    out = img.resize((W, H), Image.LANCZOS)
    out.save(os.path.join(HERE, "world-map.png"), optimize=True)

    layout = {
        "_about": "Proposed world layout (24 Oct). World px on an 8,192 x 8,192 canvas, north up, centre = the "
                  "Pinnacle. Drawn from scratch; no game art. Bearings clockwise from north.",
        "canvas": [8192, 8192], "centre": [C, C],
        "rings": {"meridia_coast_r": {str(b): round(MERIDIA_R(b)) for b in range(0, 360, 5)},
                  "galeway_inner_r": {str(b): round(gale_in(b)) for b in range(0, 360, 5)},
                  "galeway_outer_r": {str(b): round(gale_out(b)) for b in range(0, 360, 5)},
                  "rim_r": {str(b): round(rim(b)) for b in range(0, 360, 5)}, "falls_width": FALLS_W},
        "quarters": {"northreach": [315, 45], "eastwater": [45, 135], "southdeep": [135, 225],
                     "westgloam": [225, 315]},
        "places": PLACES,
        "marrow_isle": {"centre": [round(MARROW[0]), round(MARROW[1])],
                        "outline_rel": MARROW_SHAPE, "features_rel": MARROW_FEATURES},
        "layers": {"cloudreach": CLOUD_RECT, "deep_shelf": SHELF_RECT},
        "routes_px": {k: round(length(v)) for k, v in ROUTES.items()},
        "routes_s_at_75px": {k: round(length(v) / SHIP_PX_S, 1) for k, v in ROUTES.items()},
        "walks_px": {k: round(length(v)) for k, v in WALKS.items()},
        "walks_s_running": {k: round(length(v) / RUN_PX_S, 1) for k, v in WALKS.items()},
    }
    with open(os.path.join(HERE, "world-layout.json"), "w", encoding="utf-8") as fh:
        json.dump(layout, fh, indent=1)
    for k, v in ROUTES.items():
        print(f"{k:32s} {length(v):7.0f} px  {length(v) / SHIP_PX_S:5.1f} s")
    for k, v in WALKS.items():
        print(f"{k:32s} {length(v):7.0f} px  {length(v) / RUN_PX_S:5.1f} s running")
    for p in PLACES:
        r = math.dist((p['x'], p['y']), (C, C))
        b = (math.degrees(math.atan2(p['x'] - C, C - p['y'])) + 360) % 360
        print(f"{p['id']:18s} bearing {b:5.1f}  r {r:6.0f}  ({p['x']},{p['y']})")
    print("rim at 92:", round(rim(92)), " galeway out at 92:", round(gale_out(92)), " Meridia E-W:",
          round(MERIDIA_R(90) + MERIDIA_R(270)), " N-S:", round(MERIDIA_R(0) + MERIDIA_R(180)))


if __name__ == "__main__":
    main()
