import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import time

class GlobalNewsSpider(scrapy.Spider):
    name = 'global'
    start_urls = ['https://globalnews.ca']

    def __init__(self, *args, **kwargs):
        super(GlobalNewsSpider, self).__init__(*args, **kwargs)
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def start_requests(self):
        # Yielding a Scrapy request to start the spider
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_with_selenium)

    def parse_with_selenium(self, response):
        self.driver.get(response.url)
        time.sleep(2)

        self.parse_items()

        self.driver.quit()

    def parse_items(self):

        sel = Selector(text=self.driver.page_source)

        items = sel.css('li.c-posts__item.c-posts__loadmore')
        print(self.driver.page_source)

        for item in items:
            yield {
                'title': item.css('span.c-posts__headlineText::text')
            }

