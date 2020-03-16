import scrapy
from bs4 import BeautifulSoup
import json
import re
from news_crawler.spiders.utils import (
    now_time, get_general_cat
)

HOST_URL = "https://udn.com"
REALTIME_URL = 'https://udn.com/api/more?page={}&id=&channelId=1&cate_id=0&type=breaknews&totalRecNo=10'
CP_NAME = '聯合新聞網'

def get_start_urls():
    urls = []
    for page in range(1, 35):
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
        data = json.loads(response.body_as_unicode())
        elements = data["lists"]
        for e in elements:
            url = HOST_URL + e["titleLink"]
            title = e["title"]
            img = e["url"]
            date = e["time"]["date"]

            yield scrapy.Request(
                url,
                callback=self.parse_page,
                meta={"title": title, "img": img, "date": date}
            )

    def parse_page(self, response):
        url = response.url

        title = response.meta["title"]
        img = response.meta["img"]
        date = response.meta["date"]

        text = response.text.split('<!-- end of articles -->')
        soup = BeautifulSoup(text[0], "lxml")
        body_elements = soup.find_all("p")
        body = [res.text.strip() for res in body_elements]
        body = [b for b in body if b != ""]
        body = "\n".join(body)
        cat = soup.find("title").text.split("|")[2].strip()
        if body[:6] != "window":
            yield {
                "title": title,
                "date": date,
                "url": url,
                "body": body,
                "img": img,
                "cat": get_general_cat(cat),
                "cp": CP_NAME
            }
        else:
            url = re.sub('.*(http.*)";.*', "\\1", body)
            yield scrapy.Request(
                url,
                callback=self.parse_page,
                meta={"title": title, "img": img, "date": date}
            )
