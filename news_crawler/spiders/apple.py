# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import datetime
from news_crawler.spiders.utils import (
    daterange, today_date, yesterday_date, get_general_cat, select_image
)

HOST_URL = 'http://tw.appledaily.com'
ARCHIVE_URL = 'http://tw.appledaily.com/appledaily/archive/{}'
CP_NAME = '蘋果日報'

def get_start_urls(start_date, end_date):
    date_strings = []
    for single_date in daterange(start_date, end_date):
        date_strings.append(single_date.strftime("%Y%m%d"))
    urls = []
    for date_str in date_strings:
        urls.append(ARCHIVE_URL.format(date_str))
    return urls

class AppleSpider(scrapy.Spider):
    name = "apple"
    
    def __init__(self, st=yesterday_date(), ed=today_date(), out='data', *args, **kwargs):
        super(AppleSpider, self).__init__(*args, **kwargs)
        try:
            start_date = datetime.datetime.strptime(st, '%Y-%m-%d')
            end_date   = datetime.datetime.strptime(ed, '%Y-%m-%d')
        except:
            raise Exception('Incorrect date format!')
        
        # get all archive pages of a specific date range
        self.start_urls = get_start_urls(start_date, end_date)
        self.directory =  out
        self.file = 'news_apple_{}_{}.json.lines'.format(st, ed)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        # get all the links in the archive page
        links = [link['href'] for link in soup.select('ul.fillup a')]
        for link in links:
            url = link
            if 'appledaily.com' not in link:
                url = HOST_URL + url
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        url = response.url
        soup = bs(response.body, 'lxml')

        img = None

        # 地產新聞
        if 'home.appledaily.com' in url:
            title = soup.select('.ncbox_cont > h1')[0].text.strip()
            date = soup.select('.nctimeshare time')[0]['datetime'][:-1]
            date = date.replace('/', '-')
            img = select_image(soup, '.articulum img')
            cat = '地產'
            body = '\n'.join([p.text.strip() for p in soup.select('.articulum p') if p.text.strip()!='']).strip()

        else:
            title = soup.select('hgroup h1')[0].text.strip()
            date = soup.select('hgroup .ndArticle_creat')[0].text.strip().split('：')[1]
            date = date.replace('/', '-')
            img = select_image(soup, '.ndAritcle_headPic img')
        
            try:
                cat = soup.select('.ndgTag .current')[0].text.strip()
            except:
                if 'adcontent' in url:
                    cat = '工商消息'

            # clean script tags
            useless_tags = ['.ndArticle_content script', '.ndArticle_moreNewlist','.ndArticle_pagePrev', '.ndArticle_pageNext']
            for tag in useless_tags:
                [e.extract() for e in soup.select(tag)]

            body = '\n'.join([p.text.strip() for p in soup.select('.ndArticle_margin p') if p.text.strip()!='']).strip()

        yield {
            'title': title,
            'date': date,
            'url': url,
            'body': body,
            'img': img,
            'cat': get_general_cat(cat),
            'cp': CP_NAME
        }
