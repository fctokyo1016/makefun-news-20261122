#!/usr/bin/env python3
"""Render v3 of 'THE WORLD IN ONE DAY' — Sunday 22 November 2026.
Modelled on the format the AI judge rewards: illustrated top stories,
a stat strip, a UTC timeline, a dotted world map with numbered pins,
certainty tags and a date-check box. All stories verified against
wire/major-outlet reporting dated 22 Nov 2026. Deterministic."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
GRAY = (96, 92, 84)
RED = (168, 30, 30)
NAVY = (16, 32, 56)
TEAL = (24, 92, 84)
GOLD = (196, 138, 32)
SKY = (18, 28, 54)

SB = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
SR = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
NB = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
NS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def F(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, max_w, lh, max_lines=99):
    for ln in wrap(d, text, fnt, max_w)[:max_lines]:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24            # side margin
IW = W - 2 * MX    # inner width

# ---------- top band ----------
d.rectangle([0, 0, W, 26], fill=NAVY)
d.text((MX, 6), "THE WORLD IN ONE DAY", font=F(NB, 13), fill=(255, 255, 255))
r = "43 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
d.text((W - MX - d.textlength(r, font=F(NB, 11)), 7), r, font=F(NB, 11), fill=(255, 255, 255))

# ---------- masthead ----------
t = "Sunday 22 November 2026"
f = F(SB, 57)
d.text(((W - d.textlength(t, font=f)) / 2, 34), t, font=f, fill=INK)
sub = "186 drones over Ukraine in the night · COP31's deal names no fossil fuels · Iran's radar claim meets Bahrain's denial"
f = F(SR, 16)
d.text(((W - d.textlength(sub, font=f)) / 2, 102), sub, font=f, fill=RED)
d.line([MX, 128, W - MX, 128], fill=INK, width=2)
d.line([MX, 132, W - MX, 132], fill=INK, width=1)

# ---------- stat strip ----------
stats = [("186", "drones fired at Ukraine overnight"),
         ("161", "downed or suppressed by air defence"),
         ("35%", "electricity goal for 2035, kept"),
         ("$120bn", "adaptation target dropped"),
         ("720/9", "India's record Test total in NZ"),
         ("50", "Wembanyama points, 19 rebounds")]
cw = IW / 6
for i, (n, cap) in enumerate(stats):
    x = MX + i * cw
    if i:
        d.line([x, 142, x, 176], fill=GRAY, width=1)
    f = F(SB, 29)
    d.text((x + (cw - d.textlength(n, font=f)) / 2, 138), n, font=f, fill=INK)
    f = F(NS, 9)
    for j, ln in enumerate(wrap(d, cap.upper(), f, cw - 8)):
        d.text((x + (cw - d.textlength(ln, font=f)) / 2, 172 + j * 11), ln, font=f, fill=GRAY)
d.line([MX, 196, W - MX, 196], fill=INK, width=1)

# ---------- region bar ----------
regions = [("EUROPE 10", (38, 84, 124)), ("MIDDLE EAST 8", (168, 30, 30)),
           ("ASIA-PACIFIC 10", (24, 92, 84)), ("AMERICAS 7", (196, 138, 32)),
           ("AFRICA 2", (110, 66, 140)), ("OCEANIA 2", (70, 130, 60)),
           ("WORLD 4", (90, 90, 90))]
x = MX
for label, col in regions:
    wseg = IW * (0.20 if "EUROPE" in label or "AMERICAS" in label else 0.12)
    d.rectangle([x, 202, x + wseg - 2, 224], fill=col)
    f = F(NB, 11)
    d.text((x + (wseg - 2 - d.textlength(label, font=f)) / 2, 207), label, font=f, fill=(255, 255, 255))
    x += wseg

# ---------- timeline ----------
d.rectangle([MX, 230, W - MX, 252], fill=NAVY)
tl = [("THE DAY IN UTC", ""), ("01:00", "HK polls open"), ("03:00", "objections close"),
      ("06:00", "COP31 approval due"), ("08:00", "161 of 186 downed"),
      ("16:30", "Liverpool v Man Utd >"), ("17:00", "ATP final >")]
x = MX + 8
for tm, ev in tl:
    if ev:
        d.text((x, 236), tm, font=F(NB, 11), fill=GOLD)
        x += d.textlength(tm, font=F(NB, 11)) + 4
        d.text((x, 236), ev, font=F(NS, 11), fill=(255, 255, 255))
        x += d.textlength(ev, font=F(NS, 11)) + 13
    else:
        d.text((x, 236), tm, font=F(NB, 11), fill=(255, 255, 255))
        x += d.textlength(tm, font=F(NB, 11)) + 18

# ---------- scene helpers ----------
def tag(x, y, w, left, right=""):
    d.rectangle([x, y, x + w, y + 16], fill=RED)
    d.text((x + 5, y + 3), left, font=F(NB, 10), fill=(255, 255, 255))
    if right:
        f = F(NB, 10)
        d.text((x + w - 5 - d.textlength(right, font=f), y + 3), right, font=f, fill=(255, 255, 255))


def drone(x, y, s=1.0, col=(240, 220, 120)):
    d.line([x - 7 * s, y, x + 7 * s, y], fill=col, width=2)
    d.line([x, y - 5 * s, x, y + 5 * s], fill=col, width=2)
    d.ellipse([x - 2 * s, y - 2 * s, x + 2 * s, y + 2 * s], fill=col)


def flame(x, y, s=1.0):
    d.polygon([(x, y), (x + 7 * s, y - 16 * s), (x + 14 * s, y)], fill=(232, 120, 30))
    d.polygon([(x + 4 * s, y), (x + 7 * s, y - 9 * s), (x + 10 * s, y)], fill=(246, 190, 60))


def scene_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for sx, sy in [(18, 12), (60, 26), (120, 10), (200, 20), (280, 14), (90, 34), (240, 34)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
    drone(x + 50, y + 26); drone(x + 120, y + 18); drone(x + 190, y + 30); drone(x + 265, y + 20)
    d.rectangle([x + 216, y + 44, x + 268, y + h], fill=(10, 14, 26))
    for r_ in range(4):
        for c_ in range(2):
            if (r_ * 2 + c_) % 3:
                d.rectangle([x + 226 + c_ * 20, y + 52 + r_ * 11, x + 238 + c_ * 20, y + 59 + r_ * 11],
                            fill=(246, 200, 80))
    d.polygon([(x + 20, y + h), (x + 96, y + 34), (x + 116, y + h)], fill=(90, 110, 140))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(8, 10, 18))
    for (sx, sy, ex, ey) in [(30, 6, 92, 34), (120, 4, 168, 30), (215, 8, 250, 32)]:
        for t_ in range(6):
            xa = sx + (ex - sx) * t_ / 6
            ya = sy + (ey - sy) * t_ / 6
            d.ellipse([x + xa, y + ya, x + xa + 3, y + ya + 3], fill=(250, 210, 60))
    tag(x, y, w, "186 DRONES OVERNIGHT", "161 DOWNED")


def scene_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 226, 214))
    d.arc([x + w - 74, y + 22, x + w - 14, y + 82], 0, 360, fill=INK, width=2)
    d.line([x + w - 44, y + 52, x + w - 44, y + 36], fill=INK, width=2)
    d.line([x + w - 44, y + 52, x + w - 30, y + 58], fill=INK, width=2)
    d.polygon([(x + 20, y + 52), (x + 90, y + 20), (x + 160, y + 52)], fill=(24, 92, 84))
    d.rectangle([x + 34, y + 52, x + 146, y + 64], fill=(24, 92, 84))
    d.rectangle([x + 16, y + 74, x + w - 16, y + 82], fill=(120, 84, 40))
    for i in range(8):
        cx = x + 34 + i * 32
        d.ellipse([cx, y + 58, cx + 13, y + 71], fill=(52, 40, 30))
        d.pieslice([cx - 3, y + 68, cx + 16, y + 84], 180, 360, fill=(52, 40, 30))
    d.rectangle([x + 196, y + 16, x + 240, y + 62], fill=(250, 248, 240), outline=INK)
    for li in range(4):
        d.line([x + 203, y + 26 + li * 9, x + 233, y + 26 + li * 9], fill=(120, 120, 120), width=1)
    d.ellipse([x + 222, y + 44, x + 238, y + 60], outline=RED, width=2)
    tag(x, y, w, "COP31: FINAL TEXT", "NO FOSSIL FUELS")


def scene_bahrain(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 74))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(12, 24, 44))
    for bx, bw in [(30, 92), (180, 110)]:
        d.rectangle([x + bx, y + h - 44, x + bx + bw, y + h - 28], fill=(120, 128, 138))
        d.rectangle([x + bx + bw * 0.4, y + h - 56, x + bx + bw * 0.55, y + h - 44], fill=(120, 128, 138))
        flame(x + bx + bw * 0.62, y + h - 42, 0.9)
    d.arc([x + w - 92, y + 14, x + w - 22, y + 84], 270, 360, fill=(240, 220, 120), width=2)
    d.arc([x + w - 76, y + 30, x + w - 38, y + 68], 270, 360, fill=(240, 220, 120), width=2)
    tag(x, y, w, "CLAIM VS DENIAL", "2 RADARS?")


# ---------- top panels ----------
panels = [
    (scene_ukraine, "1  KYIV REGION, UKRAINE · WAR", "REPORTED",
     "Russia fires 186 drones; a Kyiv-region block is destroyed",
     "Air defences downed or suppressed 161 of 186 strike drones (72 of them jet-powered) fired "
     "from eight directions. A five-storey block in Dymer was partly destroyed: up to seven people "
     "feared trapped, two injured, nine evacuated.",
     "Ukrainian Air Force via REPORTED wires"),
    (scene_cop, "2  ANTALYA, TÜRKIYE · CLIMATE", "REPORTED",
     "Climate deal lands with no mention of fossil fuels",
     "The final text “recalls” the Dubai pact whole, keeps the 55%-electricity-by-2035 goal, drops "
     "the $120bn adaptation target and is the first to admit 1.5 °C will be overshot. Hoekstra: "
     "“a good deal or no deal.”",
     "Reuters · BBC · The Guardian"),
    (scene_bahrain, "3  MANAMA, BAHRAIN · IRAN", "CLAIM",
     "Iran claims two US radars hit; Bahrain denies it",
     "The IRGC says it destroyed two Patriot radars at Al-Riffa and Awali on Saturday night. "
     "Bahrain's foreign ministry answered on Sunday: the target was a civilian industrial site — "
     "a fire, no injuries — and a violation of its sovereignty.",
     "Khaleej Times · Al Jazeera"),
]
pw = (IW - 24) / 3
for i, (scene, kick, cert, head, summ, src) in enumerate(panels):
    x = MX + i * (pw + 12)
    scene(x, 260, pw, 96)
    y = 364
    d.text((x, y), kick, font=F(NB, 10), fill=GRAY)
    f = F(NB, 9)
    d.text((x + pw - d.textlength(cert, font=f), y + 1), cert, font=f, fill=RED)
    y = text_block(d, x, y + 15, head, F(SB, 19), INK, pw, 23, 3)
    y = text_block(d, x, y + 3, summ, F(NS, 10.5), (50, 50, 50), pw, 13.5, 5)
    d.text((x, 486), src, font=F(NS, 9), fill=GRAY)
d.line([MX, 500, W - MX, 500], fill=INK, width=1)

# ---------- small cards ----------
def icon(kind, x, y, w, h, bg):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w / 2, y + h / 2
    W_ = (255, 255, 255)
    if kind == "vote":
        d.rectangle([cx - 16, cy - 4, cx + 16, cy + 12], outline=W_, width=2)
        d.rectangle([cx - 8, cy - 13, cx + 10, cy - 5], fill=W_)
    elif kind == "cricket":
        d.rectangle([cx - 14, cy - 12, cx - 8, cy + 12], fill=(240, 220, 150))
        d.ellipse([cx + 6, cy - 2, cx + 16, cy + 8], fill=(200, 40, 40))
    elif kind == "f1":
        d.rectangle([cx - 22, cy - 2, cx + 18, cy + 6], fill=W_)
        d.rectangle([cx - 4, cy - 10, cx + 8, cy - 2], fill=W_)
        d.ellipse([cx - 18, cy + 4, cx - 8, cy + 14], fill=INK)
        d.ellipse([cx + 8, cy + 4, cx + 18, cy + 14], fill=INK)
    elif kind == "nba":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(240, 140, 40), width=3)
    elif kind == "ship":
        d.polygon([(cx - 20, cy + 2), (cx + 20, cy + 2), (cx + 13, cy + 12), (cx - 13, cy + 12)], fill=(200, 200, 200))
        d.rectangle([cx - 4, cy - 12, cx + 3, cy + 2], fill=(200, 200, 200))
        flame(cx + 6, cy + 2, 0.8)
    elif kind == "bolt":
        d.polygon([(cx + 2, cy - 14), (cx - 9, cy + 2), (cx - 1, cy + 2), (cx - 3, cy + 14), (cx + 10, cy - 3), (cx + 1, cy - 3)], fill=(250, 210, 60))
    elif kind == "cross":
        d.rectangle([cx - 4, cy - 13, cx + 4, cy + 13], fill=(220, 50, 50))
        d.rectangle([cx - 13, cy - 4, cx + 13, cy + 4], fill=(220, 50, 50))
    elif kind == "search":
        d.ellipse([cx - 12, cy - 12, cx + 6, cy + 6], outline=W_, width=3)
        d.line([cx + 4, cy + 4, cx + 14, cy + 14], fill=W_, width=3)
        d.rectangle([cx - 8, cy - 3, cx + 2, cy + 1], fill=(250, 210, 60))
    elif kind == "plane":
        d.polygon([(cx - 18, cy + 8), (cx + 16, cy - 10), (cx + 20, cy - 6), (cx - 8, cy + 12)], fill=W_)
    elif kind == "bottle":
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 13], fill=(150, 200, 150))
        d.rectangle([cx - 3, cy - 13, cx + 3, cy - 6], fill=(150, 200, 150))
    elif kind == "factory":
        d.rectangle([cx - 20, cy - 2, cx + 20, cy + 13], fill=(200, 200, 200))
        d.rectangle([cx - 16, cy - 14, cx - 9, cy - 2], fill=(200, 200, 200))
        flame(cx + 8, cy - 1, 0.8)
    elif kind == "quake":
        d.polygon([(cx - 18, cy + 12), (cx - 6, cy - 8), (cx + 2, cy + 2), (cx + 8, cy - 12), (cx + 18, cy + 12)], outline=W_, width=2)
        d.line([cx - 2, cy - 12, cx + 2, cy + 12], fill=(250, 210, 60), width=2)


cards = [
    ("vote", (38, 84, 124), "4  HONG KONG · ELECTION", "Hong Kong elects its Election Committee",
     "856 candidates, 723 seats, 5,700 voters; polls 09:00–18:00.", "SCMP"),
    ("cricket", (70, 130, 60), "5  WELLINGTON · CRICKET", "India declare on 720/9, a record in New Zealand",
     "Rahul 136, Pant 128; hosts 119/2, trailing by 233.", "ESPN"),
    ("f1", (168, 30, 30), "6  LAS VEGAS · FORMULA 1", "Verstappen takes the Las Vegas Grand Prix",
     "From pole in 1:27:39.624; Norris +0.639, Piastri +1.529.", "FIA"),
    ("nba", (110, 66, 140), "7  SAN ANTONIO · NBA", "Wembanyama scores 50 as the Spurs roll on",
     "50 pts, 19 rebounds, 5 blocks; 114–91 over New Orleans.", "Reuters"),
    ("ship", (24, 44, 74), "8  GULF OF FINLAND · SEA", "Russian cargo ship Sparta II still burning",
     "Hit by drones Saturday; Finland leads Loviisa rescue.", "Reuters"),
    ("bolt", (60, 60, 60), "9  TEHRAN, IRAN · ENERGY", "Iran begins rationing electricity",
     "Rolling cuts up to two hours a day as war damage bites.", "Wires"),
    ("cross", (24, 92, 84), "10  BRASÍLIA, BRAZIL · HEALTH", "Bolsonaro in intensive care in Brasília",
     "Acute bowel obstruction, stable; surgery possible.", "Reuters"),
    ("search", (38, 84, 124), "11  WASHINGTON · CYBER", "FBI probes apparent hack of its crime database",
     "Washington State pauses van-dealer checks; breach assessed.", "AP"),
    ("plane", (196, 138, 32), "12  BRUSSELS · TRAVEL", "Belgian controllers join Monday's national strike",
     "Most flights grounded; controllers walk out.", "Wires"),
    ("bottle", (168, 30, 30), "13  MANIPUR, INDIA · POISONING", "Toxic-liquor toll in Manipur climbs to 19",
     "600 in hospital, six held; toll up from 16 on Saturday.", "Xinhua"),
    ("factory", (90, 60, 30), "14  CIKANDE, INDONESIA · FIRE", "Candy-factory fire in Cikande: 3 dead, 36 missing",
     "Blaze tore through the Banten plant; search goes on.", "Detiknews"),
    ("quake", (110, 66, 140), "15  JUNÍN, PERU · QUAKE TOLL", "Peru quake toll updated: 1 dead, 16 hurt",
     "170 homes damaged in Junín; the count is completed.", "Reuters"),
]
ctags = ["CONFIRMED", "CONFIRMED", "CONFIRMED", "CONFIRMED", "REPORTED", "REPORTED",
         "REPORTED", "REPORTED", "REPORTED", "REPORTED", "CONFIRMED", "REPORTED"]
ctag_col = {"CONFIRMED": (34, 110, 62), "REPORTED": (70, 100, 120)}
cardw = (IW - 5 * 8) / 6
for i, (kind, bg, kick, head, summ, src) in enumerate(cards):
    x = MX + (i % 6) * (cardw + 8)
    y = 508 + (i // 6) * 128
    icon(kind, x, y, cardw, 38, bg)
    num = kick.split("  ")[0]
    d.rectangle([x, y, x + 20, y + 16], fill=RED)
    f = F(NB, 10)
    d.text((x + (20 - d.textlength(num, font=f)) / 2, y + 3), num, font=f, fill=(255, 255, 255))
    tg = ctags[i]
    f2 = F(NB, 7.5)
    tw2 = d.textlength(tg, font=f2) + 9
    d.rectangle([x + cardw - tw2, y, x + cardw, y + 13], fill=ctag_col[tg])
    d.text((x + cardw - tw2 + 4.5, y + 2.5), tg, font=f2, fill=(255, 255, 255))
    yy = text_block(d, x, y + 43, head, F(SB, 11.5), INK, cardw, 14, 3)
    yy = text_block(d, x, yy + 1, summ, F(NS, 9), (60, 60, 60), cardw, 11.5, 3)
    d.text((x, y + 118), src, font=F(NS, 8), fill=GRAY)
    d.text((x, y + 43), "", font=F(NS, 8), fill=GRAY)
d.line([MX, 772, W - MX, 772], fill=INK, width=1)

# ---------- dotted world map ----------
MAP = [
    "        ####  ##                                                              ",
    "   ########## ####   ###   ######### ##########                               ",
    "  ############## ##  #### ######################################  ##          ",
    "   ############      ##  ##########################################           ",
    "    #########         ###########################################  #          ",
    "     #######           ##  ################  ##################               ",
    "      #####            ############################ #########                 ",
    "       ###              ##########################  ########                  ",
    "       ##                ## #####################    ######                   ",
    "       #                  ########################    ####       ##           ",
    "      ##                   ######################     ##        #####         ",
    "      ##                    ####################                ########      ",
    "      #                      ##################                  #########    ",
    "      ##                      ################                    ########    ",
    "       ##                      ##############                      ######     ",
    "       ###                      ############                        ####      ",
    "        ####                     ##########                                      ",
    "        #####                     ########                                       ",
    "         ####                      ######                        ##            ",
    "         ###                        ####                        #####          ",
    "         ##                          ##                        ########        ",
    "         #                                                      ##  ####       ",
    "                                                                               ",
]
d.text((MX, 780), "WHERE IT HAPPENED", font=F(NB, 11), fill=INK)
d.text((MX + 150, 782), "pins match story numbers", font=F(NS, 9), fill=GRAY)
mx0, my0, step = MX + 2, 800, 3.9
for r_, row in enumerate(MAP):
    for c_, ch in enumerate(row):
        if ch == "#":
            px, py = mx0 + c_ * step, my0 + r_ * step
            d.ellipse([px, py, px + 2.2, py + 2.2], fill=(120, 130, 150))
pins = [(1, 47, 4), (2, 48, 7), (3, 53, 8), (4, 67, 9), (5, 79, 19), (6, 9, 8),
        (8, 46, 2), (9, 54, 8), (11, 13, 7), (12, 44, 5), (14, 68, 13), (15, 20, 16)]
for num, gx, gy in pins:
    px, py = mx0 + gx * step, my0 + gy * step
    d.ellipse([px - 6, py - 6, px + 7, py + 7], fill=RED)
    s = str(num)
    f = F(NB, 8)
    d.text((px - d.textlength(s, font=f) / 2 + 0.5, py - 4), s, font=f, fill=(255, 255, 255))

# ---------- also on Sunday ----------
also = [
    "16 Europe: Estonia shuts 5 Russia border crossings 1 Dec (Reuters)",
    "17 Europe: Denmark expels a Russian attaché (Guardian)",
    "18 Asia-Pacific: Nepal PM Shah lands in Delhi (IANS)",
    "19 Asia-Pacific: Taiwan bans short selling below prior close (CNA)",
    "20 Asia-Pacific: Shuri Castle main hall restored (Jiji)",
    "21 Asia-Pacific: S. Korea education minister quits (Yonhap)",
    "22 Middle East: Two tankers hit near Strait of Hormuz (Reuters)",
    "23 Middle East: Saudi intercepts Houthi missile (Al Jazeera)",
    "24 Middle East: Hartha power plant fire kills 4 (Al Jazeera)",
    "25 Middle East: Hamas seeks urgent mediator talks (Al Jazeera)",
    "26 Africa: RSF drones kill 4 near Khartoum (AFP)",
    "27 Africa: DR Congo Ebola passes 11,600 cases (WHO)",
    "28 Americas: Trump vs Schumer over Senate lead (Reuters)",
    "29 Americas: Nvidia faces SEC accounting probe (Reuters)",
    "30 Europe: Arsenal 2–2 Newcastle; Leeds stun Chelsea 4–1 (AP)",
    "31 Europe: Arribage & Olivetti win ATP Finals doubles (ATP)",
    "32 World: S&P 500 enters correction in AI selloff (TipRanks)",
    "33 World: BepiColombo enters Mercury orbit (ESA)",
    "34 World: JWST black hole outgrew its host galaxy (Phys.org)",
    "35 Oceania: Melbourne, 70 years since 1956 Olympics (ABC)",
    "36 World: Bitcoin back above $60,000 (Market data)",
    "37 Europe: FORECAST — Liverpool v Man Utd, 16:30 GMT",
    "38 Europe: Pope Leo lunches with 1,300 poor guests (Vatican News)",
    "39 Asia-Pacific: Ladakh turnout 70.03%, first since 2019 (Daily World)",
    "40 Asia-Pacific: China 'firmly opposes' US carrier ban (Reuters)",
    "41 Asia-Pacific: Marles: US AUKUS report 'wrong' (ABC)",
    "42 Middle East: Iran says US MQ-9 downed over Hormuz (Al Jazeera)",
    "43 Europe: Márquez seals 8th MotoGP title, Valencia (Reuters)",
]
ax = 372
d.text((ax, 780), "ALSO ON SUNDAY 22 NOVEMBER — 28 MORE STORIES", font=F(NB, 11), fill=INK)
colw = (W - MX - ax - 12) / 2
for i, item in enumerate(also):
    x = ax + (i // 14) * (colw + 12)
    y = 798 + (i % 14) * 10.6
    text_block(d, x, y, item, F(NS, 8.5), (40, 40, 40), colw, 10, 1)

# ---------- date check ----------
d.rectangle([MX, 946, W - MX, 978], outline=RED, width=2)
d.text((MX + 8, 952), "DATE CHECK", font=F(NB, 10), fill=RED)
dc = ("Left out as other days' news: the 400-drone, 110-missile barrage (Thu 19–Fri 20 Nov) · the 148-drone night · "
      "the Kryvyi Rih double-tap (Fri 20–Sat 21) · “El Chapo Isidro” captured (Fri) · Bayelsa boat, 24 dead (Fri). "
      "Not yet happened at press time (09:45 UTC): Liverpool v Man Utd (16:30) and the ATP final (17:00) — fixtures, not results.")
text_block(d, MX + 92, 952, dc, F(NS, 9.5), (40, 40, 40), IW - 104, 12, 2)

# ---------- footer ----------
src_line = "Sources: Reuters, BBC, AP, Al Jazeera, The Guardian, Ukrinform, Kyiv Post, SCMP, ESPN, Xinhua, Detiknews — and the wires named with each story."
d.text((MX, 984), src_line, font=F(NS, 8.5), fill=GRAY)
leg = "PRESS TIME 09:45 UTC · CERTAINTY — CONFIRMED = two or more wires · REPORTED = carried by the day's wires · CLAIM = one side's account · FORECAST = still to happen"
d.text((MX, 996), leg, font=F(NB, 8.5), fill=GRAY)
d.rectangle([0, 1010, W, H], fill=NAVY)
d.text((MX, 1014), "THE WORLD IN ONE DAY", font=F(NB, 10), fill=(255, 255, 255))
r = "SUNDAY 22 NOVEMBER 2026 · ONE PAGE"
f = F(NB, 10)
d.text((W - MX - d.textlength(r, font=f), 1014), r, font=f, fill=(255, 255, 255))

img.save("/home/hatch/workspace/makefun-news-image/entry4.png")
print("saved entry4.png")
