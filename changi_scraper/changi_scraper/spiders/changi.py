import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

class ChangiSpider(scrapy.Spider):
    name = "jewelchangi"
    allowed_domains = ["www.jewelchangiairport.com"]
    start_urls = ["https://www.jewelchangiairport.com"]
    custom_settings = {
        "DEPTH_LIMIT": 4,  # Limit crawl depth
        "CLOSESPIDER_PAGECOUNT": 2000,  # Limit to 50 pages
        "USER_AGENT": "Mozilla/5.0",
        "DOWNLOAD_DELAY": 1,  # 1-second delay between requests
        "CONCURRENT_REQUESTS": 8,  # Moderate concurrency
    }
    page_count = 0

    def parse(self, response):
        self.page_count += 1
        self.logger.info(f"Scraped {self.page_count}/50: {response.url}")

        # Extract text from relevant tags
        content = []
        for element in response.css("h1, h2, h3, p, li"):
            text = element.css("::text").get(default="").strip()
            if text:
                content.append(text)

        # Save content
        yield {
            "url": response.url,
            "content": content,
        }

        # Follow links within depth and page limit
        if self.page_count < self.custom_settings["CLOSESPIDER_PAGECOUNT"]:
            link_extractor = LinkExtractor(allow_domains=self.allowed_domains)
            for link in link_extractor.extract_links(response):
                yield response.follow(link.url, callback=self.parse)