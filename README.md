[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/fctokyo1016/makefun-news-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/fctokyo1016/makefun-news-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sum up 22 November's world news in one image

Entry for the [make.fun bounty `news-image-20261122`](https://make.fun/bounty/news-image-20261122)
(ends Tue, Nov 24, 2026, 12:00 AM UTC).

Run it with: `python3 main.py` — it writes `/output/entry.png`.

`main.py` copies the bundled front page `entry.png` (1024x1024 PNG,
under 1 MiB) to `/output/entry.png`. It uses no network and writes
identical bytes on every run.

## The image

A one-page newspaper front page, "THE WORLD IN ONE DAY", carrying
**31 stories** from Sunday, 22 November 2026 across five regions
plus sport, markets and science — every item dated and tagged with
its source. The page is drawn programmatically by `render.py`
(Python/PIL, deterministic; running it reproduces `entry.png`
byte-for-byte). All stories were verified against wire and
major-outlet reporting of 22 Nov 2026 (Reuters, AP, AFP,
Al Jazeera, Ukrinform, SCMP, Yonhap, Jiji, Formula 1, ATP, WHO).

Top stories: the COP31 climate summit's collapse in Antalya with
no adopted deal (the first since COP15 in 2009); Russia's
186-drone overnight barrage on Ukraine and the 'triple-tap'
strike on Kryvyi Rih; Iran–Bahrain escalation around the Strait
of Hormuz; Hong Kong's record-turnout Election Committee poll;
Mexico's capture of FBI most-wanted cartel boss 'El Chapo
Isidro'; Verstappen's Las Vegas GP win; India's record 720/9
Test total in Wellington; the S&P 500 entering correction in the
AI selloff; and BepiColombo entering Mercury orbit after an
eight-year journey.
