# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/3840633835/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/3840633835/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page that sums up the world news of Wednesday 25 November 2026 in a single 1024×1024 image: 30 real, dated stories — Pakistan's first astronaut flying to Tiangong aboard Shenzhou-24, two oil tankers hit by mines in the Strait of Hormuz, Asia's chip stocks crashing, the Australia–Solomon Islands security treaty, the Huawei jury verdict, Senegal regaining the AFCON title, and 19 more — with three large drawn scenes, eight small drawn scenes, a numbered world map, a stat strip and a date-check box. Every scene is drawn in code; there are no photographs.

![Wednesday 25 November 2026 — front page](screenshots/entry.png)

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That copies `entry.png` to `out/entry.png`. The entrypoint is standard-library only, as the grader requires: it copies the image the repository holds, exactly the simplest entry the competition rules describe.

To redraw the image from scratch (needs Pillow, dev machine only):

```sh
pip install pillow
python3 generate.py
```

`generate.py` is fully deterministic — same bytes on every run. See [METHODOLOGY.md](METHODOLOGY.md) for how the news was researched, the design, and the verification.

---

<sub>Entered on [make.fun](https://make.fun/?ref=brisk-lark-63-4025&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
