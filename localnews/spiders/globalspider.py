import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from selenium.webdriver.support import expected_conditions as EC
import time

class GlobalNewsSpider(scrapy.Spider):
    name = 'global'
    start_urls = ['https://globalnews.ca']
    scraped = {}
    loads_expected = 20
    articles_a_tags = []

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

        try:
            load_more_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'home-latestStories-button'))
            )
            
            for i in range(self.loads_expected):
                self.driver.execute_script("arguments[0].click();", load_more_button)
                
            time.sleep(2)
        except Exception as e:
            self.logger.error(f"\n\n\n\n\n\nError clicking the button: {e}\n\n\n\n\n\n")

        sel = Selector(text=self.driver.page_source)
        items = sel.css('li.c-posts__item.c-posts__loadmore')

        if not items:
            print("No items found using the selector!")

        for item in items:
            title = item.css('span.c-posts__headlineText::text').get()
            description = item.css('div.c-posts__excerpt::text').get()
            link = item.css('a.c-posts__inner::attr(href)').get()

            item = {
                'title': title,
                'description': description,
                'link': link
            }

            if title is None:
                continue


            if title in self.scraped:
                continue
            else:
                self.scraped[title] = True

            yield response.follow(link, callback=self.get_article, meta={'item': item})

        self.driver.quit()

    def get_article(self, response):
        item = response.meta['item']
        text_blocks = response.css('article.l-article__text.js-story-text p')
        text = self.connect_blocks(text_blocks=text_blocks)
        item['article'] = text

        yield item


    def connect_blocks(self, text_blocks):
        text = ""
        for p in text_blocks:
            new_text = ""

            for element in p.xpath('./*|./text()'):

                    # Ignore <script> or any other unwanted tags
                if element.xpath('name()').get() == 'script':
                    continue  # Skip <script> tags

                # Check if it's an <a> tag (even if nested in other tags like <em>)
                if element.xpath('name()').get() == 'a':
                    new_text += ' ' + element.xpath('.//text()').get() + ' '

                # Handle text nodes directly
                elif element.xpath('name()').get() is None:
                    new_text += element.get()




                # if element.xpath('name()').get() == 'a':  # Checks if the element is an <a> tag
                #     new_text += element.xpath('.//text()').get()
                # else:
                #     # It's a text node
                #     new_text += element.get() 




                # if element.root.tag == 'a':
                #     new_text += ' ' + element.xpath('.//text()').get() + ' '
                # elif element.root.tag == 'p':
                #     print("Paragraph text:", element.xpath('.//text()').get())
                # else:
                #     new_text += element.get()
            text += new_text 
            text += '\n\n'
        return text
       
