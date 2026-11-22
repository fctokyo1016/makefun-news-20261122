#!/usr/bin/env python3
"""Render 'THE WORLD IN ONE DAY' — a newspaper front page summing up
Sunday 22 November 2026 world news in one 1024x1024 image.

Every story below was verified against wire/major-outlet reporting
dated 22 Nov 2026 (see the source tag on each item). Deterministic:
no network, no randomness — same bytes on every run.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
GRAY = (96, 92, 84)
ACCENT = (146, 26, 26)
RULE = (40, 40, 40)

SERIF_BOLD = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
SANS_BOLD = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
SANS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# (headline, summary, source)
TOP_MAIN = ("COP31 collapses in Antalya as EU rejects deal omitting fossil fuels",
            "The climate talks ended with no deal after a record 44 hours of overtime — the first "
            "summit breakdown since COP15 in 2009, as the EU and allies refused a text with no "
            "fossil-fuel phase-out language.", "AFP")
TOP_SIDE = [
    ("Russia launches 186 drones at Ukraine overnight; 161 downed",
     "Ukraine's Air Force says 72 were jet-powered; hits recorded at 18 sites.", "Ukrinform"),
    ("'Triple-tap' strike on Zelenskyy's hometown kills 2, wounds 60",
     "Missiles, then drones, hit rescuers in Kryvyi Rih; a boy of 7 and a paramedic died.", "Al Jazeera"),
]

EUROPE = [
    ("Drone collapses Kyiv-region apartment block; 14 missing",
     "A Russian drone partly collapsed a five-storey block in Dymer early Sunday; rescuers searched the rubble.", "Kyiv Independent"),
    ("Russian cargo ship Sparta II still burning off Finland",
     "Likely hit by Ukrainian drones Saturday, the Kaliningrad-bound ship drifted into Finnish waters; crew evacuated.", "Al Jazeera"),
]
AFRICA = [
    ("Funeral boat capsizes in Nigeria; at least 24 dead",
     "The overcrowded boat sank travelling Ayama to Ukubie in Bayelsa State; 24 people were rescued.", "AP / Al Jazeera"),
    ("RSF drone attacks kill 4 near Khartoum, damage UN building",
     "Pre-dawn Sunday strikes hit homes and a UN premises with staff inside in Omdurman.", "AFP / Al Jazeera"),
    ("DR Congo Ebola outbreak passes 11,600 cases",
     "The Bundibugyo strain has killed 5,678 across eight provinces; WHO keeps the emergency in place.", "WHO / Africa CDC"),
]
MIDDLE_EAST = [
    ("Iran's IRGC claims strikes on US Patriot radars in Bahrain",
     "Tehran says missiles and drones hit radars at Al-Riffa and Awali bases; damage not confirmed by the US.", "Al Jazeera"),
    ("Bahrain says Iranian attack set Sitra facility ablaze",
     "Manama denies US bases were hit and says a civilian industrial site burned; two people were hurt.", "Khaleej Times"),
    ("Two tankers hit by projectiles near the Strait of Hormuz",
     "UKMTO reports strikes off Oman's Khasab; at least 25 tankers hit around Hormuz in seven days.", "Reuters"),
    ("Saudi-led coalition intercepts Houthi ballistic missile",
     "The missile from Yemen was destroyed over western Saudi Arabia; a Mecca alert was briefly issued.", "Al Jazeera"),
    ("Fire at Iraq's Hartha power plant kills 4, injures 35",
     "The blaze at the 800 MW Basra station spread to nearby homes and forced a shutdown.", "Al Jazeera"),
    ("Israeli attacks kill 3 Gazans despite ceasefire, medics say",
     "A drone bomb near Deir al-Balah killed a 50-year-old man; two others died of earlier wounds.", "Anadolu"),
]
ASIA_PACIFIC = [
    ("Hong Kong Election Committee poll draws record 98.79% turnout",
     "5,640 of 5,709 eligible voters cast ballots; 856 candidates contested 723 seats in 31 subsectors.", "SCMP"),
    ("Fire at Indonesian candy factory kills 3, leaves 36 missing",
     "The blaze at the Fonusa Agung Mulia plant in Banten, near Jakarta; 15 workers were rescued.", "AP / Al Jazeera"),
    ("Taiwan bans short selling below prior close amid AI rout",
     "The first blanket curb since 2015 follows Friday's 6.23% Taiex plunge; margin raised to 150%.", "TaiwanPlus / CNA"),
    ("Shuri Castle's main hall restored, seven years after fire",
     "A completion ceremony was held Sunday in Naha, Okinawa; the Seiden opens to the public Monday.", "Jiji / Japan Times"),
    ("South Korea's education minister quits over exam chaos",
     "Choi Kyo-jin resigned over last-minute anti-cheating rule changes for the CSAT; 111 device cases caught.", "Yonhap"),
]
AMERICAS = [
    ("Mexico captures FBI most-wanted cartel boss 'El Chapo Isidro'",
     "The Guasave, Sinaloa raid killed 11 — four soldiers and seven gunmen; a $5m US reward was on Meza Flores.", "AP"),
    ("Peru counts Junín quake toll: 1 dead, 16 injured, 853 displaced",
     "The magnitude 6.7 quake struck Friday; a magnitude 5.0 aftershock followed on Sunday.", "AP / USGS"),
    ("Trump: hard to work with Schumer if he leads the Senate",
     "Democrats won both chambers in the Nov 3 midterms; Schumer faces a challenge from Van Hollen.", "Reuters"),
]
SPORT = [
    ("Verstappen wins Las Vegas GP thriller by 0.639 seconds",
     "Career win No. 75 after 35 lead changes; Norris second, Piastri third.", "Formula 1"),
    ("India declare at record 720/9 in Wellington Test",
     "Rahul 136, Pant 128 — the highest Test total ever in NZ; NZ 119/2, trailing by 233.", "Indian Express"),
    ("Leaders Arsenal held 2-2 at Newcastle",
     "Madueke levelled on 78 minutes; Arsenal stay top with 28 points.", "AP"),
    ("Leeds stun Chelsea 4-1 at Stamford Bridge",
     "Okafor scored twice in Leeds' first league win there since 1999.", "ETV Bharat"),
    ("Arribage and Olivetti win ATP Finals doubles title",
     "The French sixth seeds beat Arevalo/Pavic 3-6 7-6 10-6 in Turin.", "ATP Tour"),
]
MARKETS_SCIENCE = [
    ("S&P 500 enters correction as AI selloff deepens",
     "Down 3.7% Friday to 6,910 and 8.6% on the week; the Nasdaq 100 fell 10%.", "TipRanks"),
    ("Nvidia sinks 22.9% in a week amid SEC probe reports",
     "Reuters reported SEC staff are examining Nvidia's accounting; shares fell about 14% Friday.", "Reuters"),
    ("BepiColombo enters Mercury orbit after eight-year journey",
     "Only the second craft ever to orbit Mercury; the ESA and JAXA probes separate Dec 9-10.", "Chosun Biz / ESA"),
    ("JWST spots black hole that outgrew its host galaxy",
     "A 3.3-million-solar-mass black hole in galaxy MARTA-3887 grew faster than its host.", "Phys.org"),
]

N_STORIES = (1 + len(TOP_SIDE) + len(EUROPE) + len(AFRICA) + len(MIDDLE_EAST)
             + len(ASIA_PACIFIC) + len(AMERICAS) + len(SPORT) + len(MARKETS_SCIENCE))


def draw_item(d, x, y, w, item, f_h, f_s, f_src, lh_h, lh_s):
    head, summ, src = item
    for ln in wrap(d, head, f_h, w):
        d.text((x, y), ln, font=f_h, fill=INK)
        y += lh_h
    for ln in wrap(d, summ, f_s, w):
        d.text((x, y), ln, font=f_s, fill=(52, 50, 46))
        y += lh_s
    d.text((x, y), "— " + src.upper(), font=f_src, fill=GRAY)
    return y + lh_s + 5


def section_header(d, x, y, w, title, f_sec, fill=INK):
    d.rectangle([x, y, x + w, y + 17], fill=fill)
    d.text((x + 6, y + 2), title, font=f_sec, fill=PAPER)
    return y + 23


def draw_section(d, x, y, w, title, items, F):
    f_sec, f_h, f_s, f_src, lh_h, lh_s = F
    y = section_header(d, x, y, w, title, f_sec)
    for it in items:
        y = draw_item(d, x, y, w, it, f_h, f_s, f_src, lh_h, lh_s)
    return y


def render(hs=13, ss=11, lh_h=15, lh_s=13):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    f_title = font(SERIF_BOLD, 50)
    f_sub = font(SANS_BOLD, 14)
    f_sec = font(SANS_BOLD, 12)
    f_h = font(SANS_BOLD, hs)
    f_s = font(SANS, ss)
    f_src = font(SANS_BOLD, 9)
    f_top = font(SERIF_BOLD, 26)
    f_toph = font(SANS_BOLD, 15)
    F = (f_sec, f_h, f_s, f_src, lh_h, lh_s)

    # Masthead
    d.text((M, 8), "THE WORLD IN ONE DAY", font=f_title, fill=INK)
    d.line([M, 72, W - M, 72], fill=RULE, width=3)
    d.text((M, 78), f"Sunday, 22 November 2026  ·  {N_STORIES} stories  ·  5 regions + sport, markets & science  ·  every item dated and sourced",
           font=f_sub, fill=ACCENT)
    d.line([M, 102, W - M, 102], fill=RULE, width=1)

    # Top band
    y = 112
    left_w = 596
    head, summ, src = TOP_MAIN
    yy = y
    for ln in wrap(d, head, f_top, left_w):
        d.text((M, yy), ln, font=f_top, fill=INK)
        yy += 32
    for ln in wrap(d, summ, f_s, left_w):
        d.text((M, yy), ln, font=f_s, fill=(52, 50, 46))
        yy += lh_s
    d.text((M, yy), "— " + src.upper(), font=f_src, fill=GRAY)
    sx = M + left_w + 22
    sw = W - M - sx
    d.line([sx - 11, y, sx - 11, y + 138], fill=RULE, width=1)
    sy = y
    for it in TOP_SIDE:
        sy = draw_item(d, sx, sy, sw, it, f_toph, f_s, f_src, 18, lh_s)
    top_end = max(yy + 14, sy)
    d.line([M, top_end + 2, W - M, top_end + 2], fill=RULE, width=1)

    # Main columns
    cy = top_end + 10
    col_w = (W - 2 * M - 2 * 16) // 3
    xs = [M, M + col_w + 16, M + 2 * (col_w + 16)]
    e = draw_section(d, xs[0], cy, col_w, "EUROPE", EUROPE, F)
    e = draw_section(d, xs[0], e + 2, col_w, "AFRICA", AFRICA, F)
    e2 = draw_section(d, xs[1], cy, col_w, "MIDDLE EAST", MIDDLE_EAST, F)
    e3 = draw_section(d, xs[2], cy, col_w, "ASIA-PACIFIC", ASIA_PACIFIC, F)
    main_end = max(e, e2, e3)

    # Bottom band: SPORT · MARKETS · SCIENCE flowing in 3 columns
    by = main_end + 4
    d.line([M, by, W - M, by], fill=RULE, width=3)
    by = section_header(d, M, by + 6, W - 2 * M, "AMERICAS · SPORT · MARKETS · SCIENCE", f_sec, fill=ACCENT)
    items = AMERICAS + SPORT + MARKETS_SCIENCE
    chunks = [items[0:4], items[4:8], items[8:11]]
    row_end = by
    for i, ch in enumerate(chunks):
        yy = by
        for it in ch:
            yy = draw_item(d, xs[i], yy, col_w, it, f_h, f_s, f_src, lh_h, lh_s)
        row_end = max(row_end, yy)

    # Footer
    d.line([M, H - 38, W - M, H - 38], fill=RULE, width=1)
    d.text((M, H - 30),
           "Compiled from wire and major-outlet reporting of 22 Nov 2026 (UTC): Reuters · AP · AFP · Al Jazeera · "
           "Ukrinform · SCMP · Yonhap · Jiji · Formula 1 · ATP · WHO",
           font=font(SANS, 11), fill=GRAY)
    return img, row_end


def main():
    for hs, ss, lh_h, lh_s in ((13, 11, 15, 13), (12, 11, 14, 13), (12, 10, 14, 12),
                               (11, 10, 13, 12), (11, 10, 13, 11)):
        img, used = render(hs, ss, lh_h, lh_s)
        print(f"h={hs} s={ss}: content ends at y={used} of {H} (footer at {H-38})")
        if used <= H - 46:
            print(f"stories: {N_STORIES}")
            from pathlib import Path
            out = Path(__file__).resolve().parent / "entry.png"
            img.convert("P", palette=Image.ADAPTIVE, colors=256).save(out)
            print(f"wrote {out}")
            return
    raise SystemExit("does not fit")


if __name__ == "__main__":
    main()
