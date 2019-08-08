# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import requests
import datetime
from news_crawler.spiders.utils import (
    now_time, get_general_cat, select_image
)

# TODO: The structure of the website has been changed.
# Need to rewrite code.

HOST_URL = 'https://www.chinatimes.com'
# ARCHIVE_URL = 'http://www.chinatimes.com/history-by-date/{}-260{}?page={}'
REALTIME_URL = 'https://www.chinatimes.com/realtimenews/?page={}'
CP_NAME = '中國時報'

def get_start_urls():
    """ Get the news list urls of the 10 pages
    """
    urls = []
    for page in range(1, 11):
        urls.append(REALTIME_URL.format(page))
    return urls

def get_news_items():
    """ Retrieve news URLs from realtime news page
    """
    items = []
    for page in range(1, 11):
        r = requests.get(REALTIME_URL.format(page))
        soup = bs(r.text, 'lxml')

    rss = feedparser.parse(RSS_URL)
    items = []
    for item in rss['entries']:
        # TODO: ignore old URLs
        items.append({
            'url': item['link'],
            'date': get_tm_date(item['published_parsed'])
        })

    return items

class ChinaTimesSpider(scrapy.Spider):
    name = "chinatimes"
    
    def __init__(self, out='data', *args, **kwargs):
        super(ChinaTimesSpider, self).__init__(*args, **kwargs)
        
        # get all archive pages of a specific date range
        self.start_urls = get_start_urls()
        self.directory =  out
        self.file = 'news_{}_{}.ndjson'.format(self.name, now_time())

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        elements = soup.select('.articlebox-compact > .row > .col')
        
        # filter out ads
        elements = [e for e in elements if e.select_one('.meta-info')]

        for e in elements:
            url = HOST_URL + e.select_one('.title a')['href']
            date = e.select_one('.meta-info time')['datetime']
            title = e.select_one('.title').text.strip()

            yield scrapy.Request(
                url,
                callback=self.parse_page,
                meta={'date': date, 'title': title}
            )

    def parse_page(self, response):
        soup = bs(response.body, 'lxml')
        
        date = response.meta['date']
        title = response.meta['title']

        img = select_image(soup, 'article img')
        if img and img.startswith('//'):
            img = 'https:' + img

        cat = soup.select('.breadcrumb > .breadcrumb-item')[-1].text.strip()
        url = response.url

        body = '\n'.join([p.text.strip() for p in soup.select('article p') if p.text.strip()!='']).strip()

        yield {
            'title': title,
            'date': date,
            'url': url,
            'body': body,
            'img': img,
            'cat': get_general_cat(cat),
            'cp': CP_NAME
        }
