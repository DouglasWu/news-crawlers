import scrapy
from bs4 import BeautifulSoup
from news_crawler.spiders.utils import (
    now_time, get_general_cat
)

HOST_URL = "https://udn.com"
REALTIME_URL = 'https://udn.com/news/get_breaks_article/{}/1/0?_=1567733665389'
CP_NAME = '聯合新聞網'

def get_start_urls():
    urls = []
    for page in range(2, 12):
        urls.append(REALTIME_URL.format(page))
    return urls

class UdnCrawler(scrapy.Spider):
    name = "udn"

    def __init__(self, out='data', *args, **kwargs):
        super(UdnCrawler, self).__init__(*args, **kwargs)

        # get all archive pages of a specific date range
        self.start_urls = get_start_urls()
        self.directory = out
        self.file = 'news_{}_{}.ndjson'.format(self.name, now_time())

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        elements = soup.find_all("dt")
        for e in elements:
            url = HOST_URL + e.find("a")["href"]
            title = e.find("h2").text
            cat = e.find("a", attrs={"class": "cate"}).text
            img = e.find("img")["src"]

            yield scrapy.Request(
                url,
                callback=self.parse_page,
                meta={"title": title, "cat": cat, "img": img}
            )

    def parse_page(self, response):
        url = response.url
        soup = BeautifulSoup(response.body, "lxml")

        title = response.meta["title"]
        cat = response.meta["cat"]
        img = response.meta["img"]

        body_elements = soup.find_all("p")
        body = [res.text.strip() for res in body_elements]
        body = [b for b in body if b != ""]  # remove empty content
        body = "\n".join(body)

        date_element = soup.find("div", attrs={"class": "story_bady_info_author"})
        date = date_element.find("span").text

        yield {
            "title": title,
            "date": date,
            "url": url,
            "body": body,
            "img": img,
            "cat": get_general_cat(cat),
            "cp": CP_NAME
        }
