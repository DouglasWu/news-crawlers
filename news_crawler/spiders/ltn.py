# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from bs4 import BeautifulSoup as bs
import datetime
import re
from news_crawler.spiders.utils import (
    daterange, today_date, yesterday_date, get_general_cat, select_image
)

# TODO: The structure of the website has been changed.
# Need to rewrite code.

HOST_URL = 'https://news.ltn.com.tw'
ARCHIVE_URL = 'https://news.ltn.com.tw/list/newspaper/{}/{}'
CP_NAME = '自由時報'

def get_cat_list():
    # Retrieve the list of all news categories on the web
    url = 'https://news.ltn.com.tw/list/newspaper'
    with urllib.request.urlopen(url) as fp:
        soup = bs(fp.read(), 'lxml')
    urls = [a['href'] for a in soup.select('.newsSort.boxTitle li a')]
    return [re.match('list/newspaper/([a-z]+)', url).group(1) for url in urls]

def get_start_urls(start_date, end_date):
    date_strings = []
    for single_date in daterange(start_date, end_date):
        date_strings.append(single_date.strftime("%Y%m%d"))
    urls = []
    for date_str in date_strings:
        for cat in get_cat_list():
            urls.append(ARCHIVE_URL.format(cat, date_str))
    return urls

class LtnSpider(scrapy.Spider):
    name = "ltn"
    
    def __init__(self, st=yesterday_date(), ed=yesterday_date(), out='data', *args, **kwargs):
        super(LtnSpider, self).__init__(*args, **kwargs)
        
        # get all archive pages of a specific date range
        self.start_urls = get_start_urls(st, ed)
        self.directory =  out
        self.file = 'news_{}_{}_{}.ndjson'.format(self.name, st, ed)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        # get all the links in the archive page
        atags = soup.select('.whitecon.boxTitle ul.list li a.tit')
        links = [HOST_URL + '/' + a['href'] for a in atags]
        for link in links:
            yield scrapy.Request(link, callback=self.parse_page)

        next_page_node = soup.select('.pagination.boxTitle .p_next')
        if len(next_page_node)>0:
            next_page_url = next_page_node[0]['href']
            if next_page_url.startswith('//'):
                next_page_url = 'https:' + next_page_url
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_page(self, response):
        url = response.url

        soup = bs(response.body, 'lxml')
        [s.extract() for s in soup('script')]

        selectors = {
            'ec': {
                'title': '.whitecon.boxTitle h1',
                'date': '.whitecon.boxTitle .text .time',
                'body': '.whitecon.boxTitle .text p',
                'img': '.whitecon.boxTitle .text img',
                'cat': '財經'
            },
            'talk': {
                'title': '.conbox h1',
                'date': '.conbox .top_share .writer_date',
                'body': '.whitecon.boxTitle .text p',
                'img': '.whitecon.boxTitle .cont img',
                'cat': '評論'
            },
            'sports': {
                'title': '.news_content h1',
                'date': '.news_content .c_box .c_time',
                'body': '.whitecon.boxTitle .text p',
                'img': '.news_content img',
                'cat': '體育'
            },
            'ent': {
                'title': '.news_content h1',
                'date': '.news_content .author .date',
                'body': '.news_content p',
                'img': '.news_content img',
                'cat': '影視'
            },
            'other': {
                'title': '.whitecon.articlebody h1',
                'date': '.whitecon.articlebody .text .viewtime',
                'body': '.whitecon.articlebody .text p',
                'img': '.whitecon.articlebody .text img',
            }
        }

        if 'ec.ltn.com.tw' in url:
            # 自由財經
            selector = selectors['ec']
        elif 'talk.ltn.com.tw' in url:
            # 自由評論網
            selector = selectors['talk']
        elif 'sports.ltn.com.tw' in url:
            # 自由體育
            selector = selectors['sports']
        elif 'ent.ltn.com.tw' in url:
            # 自由娛樂
            selector = selectors['ent']
        else:
            selector = selectors['other']

        title = soup.select(selector['title'])[0].text.strip()
        date = soup.select(selector['date'])[0].text.split()[0].strip()
        date = date.replace('/', '-')
        body = '\n'.join(p.text.strip() for p in soup.select(selector['body']))
        img = select_image(soup, selector['img'])
        if 'cat' in selector:
            cat = selector['cat']
        else:
            cat = soup.select('.breadcrumbs.boxTitle a')[-1].text.strip()
        
        yield {
            'title': title,
            'date': date,
            'url': url,
            'body': body,
            'img': img,
            'cat': get_general_cat(cat),
            'cp': CP_NAME
        }
