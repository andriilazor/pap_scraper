import unicodedata
import scrapy
from pap_scraper.items import PapItem


class PapSpider(scrapy.Spider):
    name = "pap"
    allowed_domains = ["pap.pl"]
    start_urls = ["https://www.pap.pl/artykuly"]

    def __init__(self, *args, max_items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_urls = set()
        self.scraped_count = 0
        if max_items is not None:
            self.max_items = int(max_items)
        elif hasattr(self, "max_items") and self.max_items is not None:
            self.max_items = int(self.max_items)
        else:
            self.max_items = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        closespider_limit = crawler.settings.getint("CLOSESPIDER_ITEMCOUNT", 0)
        if spider.max_items is None:
            if closespider_limit > 0:
                spider.max_items = closespider_limit
            else:
                spider.max_items = 10000
        elif closespider_limit > 0:
            spider.max_items = min(spider.max_items, closespider_limit)
        return spider

    def parse(self, response):
        if self.max_items is None:
            self.max_items = 10000

        # Extract article items from news listings
        for item_node in response.css("ul.newsList li.news"):
            if self.max_items and self.scraped_count >= self.max_items:
                return

            # Title extraction with fallback cascade
            raw_title = (
                item_node.css(".title::text").get()
                or item_node.css("h2.title::text, h4.title::text").get()
                or item_node.css("a.newsLink::attr(title)").get()
            )

            # URL extraction with fallback
            raw_url = (
                item_node.css("a.newsLink::attr(href)").get()
                or item_node.css("a::attr(href)").get()
            )

            if not raw_title or not raw_url:
                continue

            raw_url = raw_url.strip()
            if raw_url.startswith("#") or raw_url.startswith("javascript:"):
                continue

            # Clean and normalize Polish text
            cleaned_title = " ".join(
                unicodedata.normalize("NFKC", raw_title).split()
            )
            if not cleaned_title:
                continue

            # Resolve relative link to absolute URL
            full_url = response.urljoin(raw_url)

            # Filter out anti-bot challenge anomalies if any
            if "_Incapsula_Resource" in full_url or "Incapsula" in cleaned_title:
                continue

            # Deduplicate items across within-page and paginated pages
            if full_url in self.seen_urls:
                continue
            self.seen_urls.add(full_url)

            yield PapItem(title=cleaned_title, url=full_url)
            self.scraped_count += 1

            if self.max_items and self.scraped_count >= self.max_items:
                return

        # Check limit before following pagination
        if self.max_items and self.scraped_count >= self.max_items:
            return

        # Follow pagination link to the next page
        next_page = (
            response.css("li.page-item.next a::attr(href)").get()
            or response.css("a[rel='next']::attr(href)").get()
        )
        if next_page:
            next_page = next_page.strip()
            if next_page and next_page != "#" and not next_page.startswith("javascript:"):
                yield response.follow(next_page, callback=self.parse)
