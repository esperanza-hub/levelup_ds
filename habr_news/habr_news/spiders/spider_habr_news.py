import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from habr_news.habr_news.items import HabrNewsItem


class spider_habr_news(scrapy.Spider):
    name = "habr_news"
    allowed_domains = ["habr.com"]
    start_urls = ["https://habr.com/ru/news/"]

    def parse(self, response):
        counter = 0
        for post in response.css("article.post_preview"):
            post_link = post.css("a.post__title_link::attr(href)")[0].root.strip()
            yield Request(post_link, callback=self.parse_post_page) #, dont_filter=True)

        for page_link in response.css("a.arrows-pagination__item-link_next::attr(href)"):
            next_page_link = "https://habr.com" + page_link.root.strip()
            yield Request(next_page_link, callback=self.parse)


    def parse_post_page(self, response):
        item = HabrNewsItem()

        item['author'] = response.css("span.user-info__nickname::text")[0].root.strip()

        item['author_karma'] = float(response.css("div.stacked-counter__value::text")[0].root.strip().replace(',', '.').replace('–', '-'))

        item['author_rating'] = float(
             response.css("div.stacked-counter__value_magenta::text")[0].root.strip().replace(',', '.').replace('–','-'))

        item['author_specialization'] = response.css("div.user-info__specialization::text")[0].root

        comments_count = response.css("span#post-stats-comments-count::text")[0].root
        if comments_count == 'Комментировать':
            comments_count = '0'
        item['comments_counter'] = int(comments_count.strip())

        hubs = []
        for hub in response.css("ul.js-post-hubs").css("a.post__tag::text"):
            hubs.append(hub.root.strip())
        item['hubs'] = hubs

        item['news_id'] = int(response.css("article.post_full::attr(id)")[0].root.strip().replace('post_', ''))

        tags = []
        for tag in response.css("ul.js-post-tags").css("a.post__tag::text"):
            tags.append(tag.root)
        item['tags'] = tags

        text = ""
        for paragraph in response.css("div#post-content-body ::text"):
            text += paragraph.root.strip().replace(u'\xa0', '').replace('\u200b', '') + ' '
        item['text'] = text

        item['title'] = response.css("span.post__title-text::text")[0].root

        yield item


if __name__ == '__main__':
    process = CrawlerProcess(settings={
        "FEEDS": {
            "news.json": {"format": "json"},
        },
        "LOG_LEVEL": "ERROR",
        "FEED_EXPORT_ENCODING": "utf-8"
    })
    process.crawl(spider_habr_news)
    process.start()  # the script will block here until the crawling is finished
