import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import time

class GlobalNewsSpider(scrapy.Spider):
    name = 'testowy'
    start_urls = ['https://globalnews.ca']

    def __init__(self, *args, **kwargs):
        super(GlobalNewsSpider, self).__init__(*args, **kwargs)
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_with_selenium)

    def parse_with_selenium(self, response):
        self.driver.get(response.url)
        time.sleep(2)

        sel = Selector(text=self.driver.page_source)
        items = sel.css('li.c-posts__item.c-posts__loadmore')

        if not items:
            print("No items found using the selector!")

        for item in items:
            title = item.css('span.c-posts__headlineText::text').get()
            description = item.css('div.c-posts__excerpt::text').get()
            
            yield {
                'title': title,
                'description': description
            }

        self.driver.quit()
