# Scrapy settings for pap_scraper project
# See https://docs.scrapy.org/en/latest/topics/settings.html

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BOT_NAME = "pap_scraper"

SPIDER_MODULES = ["pap_scraper.spiders"]
NEWSPIDER_MODULE = "pap_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Anti-bot bypass: Custom DNS resolver targeting PAP origin IP directly
DNS_RESOLVER = "pap_scraper.resolvers.PapOriginResolver"

# Concurrency and throttling settings
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 0.5

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
}

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

# Save scraped items to JSON automatically (overwrite on each run)
FEEDS = {
    str(PROJECT_ROOT / "titles.json"): {"format": "json", "overwrite": True},
}

# Only export the title field to the JSON output
FEED_EXPORT_FIELDS = ["title"]
