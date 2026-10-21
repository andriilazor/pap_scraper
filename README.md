# pap_scraper

A simple [Scrapy](https://scrapy.org/) project that collects article titles from the news listing of [pap.pl](https://www.pap.pl/artykuly), the website of the Polish Press Agency (PAP).

## How it works

- The `pap` spider starts at `https://www.pap.pl/artykuly` and reads each entry in the news list (`ul.newsList li.news`).
- For every article it extracts the title and URL, normalizes the Polish text (Unicode NFKC, collapsed whitespace), and skips duplicates and anti-bot challenge pages.
- It follows the "next page" link until it reaches the item limit (10,000 by default) or runs out of pages.
- Results are written to `titles.json`, overwriting the previous file. Only the `title` field is exported.

## Project structure

```
scrapy.cfg                  Scrapy project config
titles.json                 Output file (generated)
pap_scraper/
├── items.py                PapItem definition (title, url)
├── resolvers.py            Custom DNS resolver for pap.pl
├── settings.py             Scrapy settings and feed export config
└── spiders/
    └── pap.py              The "pap" spider
```

## Requirements

- Python 3.9+
- Scrapy

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install scrapy
```

## Usage

Run the spider from the project root:

```bash
scrapy crawl pap
```

Limit the number of scraped articles:

```bash
scrapy crawl pap -a max_items=100
```

The titles are saved to `titles.json`:

```json
[
{"title": "UE otworzyła dwa kolejne klastry dla Ukrainy. Podano szczegóły"},
{"title": "Miał planować zamach na premiera. Prokuratura: 66-latek usłyszał zarzuty"}
]
```

## Notes

- `pap_scraper/resolvers.py` maps `pap.pl` and `www.pap.pl` directly to the origin server IP (`193.200.216.72`) to bypass the Imperva Incapsula CDN challenge page. If the origin IP changes, update `ORIGIN_IP` there.
- `ROBOTSTXT_OBEY` is set to `False` in `settings.py`. Check the site's terms of use and `robots.txt` before scraping at scale.
- Requests are throttled (`DOWNLOAD_DELAY = 0.5`, 2 concurrent requests per domain) to keep the load on the server low.
