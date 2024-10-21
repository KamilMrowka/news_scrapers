import scrapy


class NewsSpider(scrapy.Spider):
    name = 'local'
    start_urls = ['https://patch.com/us/across-america/topics/patch-exclusives']

    max_scraped_pages = 20
    i = 2

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def parse(self, response):
        for articles in response.css('div.styles_Card__Content__akuyP'):
            title = articles.css('a.styles_Card__TitleLink__bKyDz::text').get()
            description = articles.css('p.styles_Card__Description__CaPcr::text').get()
            link = 'https://patch.com' + articles.css('a.styles_Card__TitleLink__bKyDz::attr(href)').get()
            item = {
                'title': title,
                'description': description,
                'link': link
            }
            yield response.follow(link, callback=self.parse_articles_text, meta={'item': item})

        if self.i <= self.max_scraped_pages:
            next_page = self.start_urls[0] + '?page=' + str(self.i)
            self.i += 1
            yield response.follow(next_page, callback=self.parse)


    def parse_articles_text(self, response):
        item = response.meta['item']
        text_blocks = response.css('div.styles_HTMLContent__LDG2k p::text').getall()
        text = self.connect_blocks(text_blocks=text_blocks)
        item['article'] = text

        yield item


    def connect_blocks(self, text_blocks):
        text = ""
        for block in text_blocks:
            text += block
            text += '\n\n'
        return text
