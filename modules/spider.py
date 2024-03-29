import re
import scrapy
from urllib.parse import urlparse
from scrapy import signals
from .database import CrawledDomains, CrawledPages, get_db
from sqlalchemy.orm import Session

# Define a Scrapy spider using Pyppeteer for JavaScript rendering.
class PyppeteerSpider(scrapy.Spider):
    name = 'pyppeteer_spider' # Name of the spider.
    page_count = 0 # Counter to track the number of pages crawled.
    max_pages = 10 # Maximum number of pages to crawl.

    # Class method to connect the spider_closed method to the spider_closed signal.
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PyppeteerSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    # Initialize the spider, setting the domain_id to None.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_id = None

    # Callback method when the spider is closed. Updates the domain's status in the database.
    def spider_closed(self, spider, reason):
        db = next(get_db())
        status = 'COMPLETED' if reason == 'finished' else 'FAILURE'
        if self.domain_id:
            domain = db.query(CrawledDomains).filter(CrawledDomains.id == self.domain_id).first()
            if domain:
                domain.status = status
                db.commit()
        db.close()

    # Method to generate the initial requests for the spider.
    def start_requests(self):
        db = next(get_db())
        for url in self.start_urls:
            domain_url = urlparse(url).netloc

            domain = db.query(CrawledDomains).filter(CrawledDomains.domain_url == domain_url).first()
            if domain:
                domain.status = 'PENDING'
                db.commit()
            else:
                domain = CrawledDomains(domain_url=domain_url, status='PENDING')
                db.add(domain)
                db.commit()
            
            self.domain_id = domain.id
            yield scrapy.Request(url, meta={'pyppeteer': True, 'domain_id': domain.id})
        db.close()

    # Method to parse the responses from the requests made by the spider.
    def parse(self, response):
        db = next(get_db())
        if self.page_count < self.max_pages:
            self.page_count += 1
            visible_texts = response.xpath('//body//*[not(self::script or self::style or self::meta or self::link)]/text()').getall()
            clean_text = ' '.join([re.sub(r'\s+', ' ', node).strip() for node in visible_texts if node.strip()])
            
            page = db.query(CrawledPages).filter(CrawledPages.page_url == response.url).first()
            if page:
                page.content = clean_text
            else:
                page = CrawledPages(page_url=response.url, content=clean_text, crawled_domain_id=response.meta['domain_id'])
                db.add(page)
            db.commit()

            current_domain = urlparse(response.url).netloc
            for a in response.css('a::attr(href)'):
                link = a.extract()
                link_domain = urlparse(link).netloc
                if current_domain == link_domain or not link_domain:
                    yield response.follow(a, self.parse, meta={'domain_id': response.meta['domain_id']})
        db.close()