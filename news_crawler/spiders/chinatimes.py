# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import datetime
from news_crawler.spiders.utils import daterange, today_date, yesterday_date, get_general_cat

host_url = 'http://www.chinatimes.com';
archive_url = 'http://www.chinatimes.com/history-by-date/{}-260{}?page={}'

def get_start_urls(start_date, end_date):
    date_strings = []
    for single_date in daterange(start_date, end_date):
        date_strings.append(single_date.strftime("%Y-%m-%d"))
    urls = []
    for date_str in date_strings:
        for aid in range(1,5):
            urls.append(archive_url.format(date_str, aid, 1))
    return urls

class ChinaTimesSpider(scrapy.Spider):
    name = "chinatimes"
    
    def __init__(self, st=yesterday_date(), ed=today_date(), out='data', *args, **kwargs):
        super(ChinaTimesSpider, self).__init__(*args, **kwargs)
        try:
            start_date = datetime.datetime.strptime(st, '%Y-%m-%d')
            end_date   = datetime.datetime.strptime(ed, '%Y-%m-%d')
        except:
            raise Exception('Incorrect date format!')
        
        # get all archive pages of a specific date range
        self.start_urls = get_start_urls(start_date, end_date)
        self.directory =  out
        self.file = 'news_chinatimes_{}_{}.json.lines'.format(st, ed)

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        # get all the links in the archive page
        links = [host_url+link['href'] for link in soup.select('.listRight li h2 a')]
        for link in links:
            yield scrapy.Request(link, callback=self.parse_page)

        cur_page = int(response.url.split('=')[1])
        total_page = int(soup.select('.pagination li a')[-1]['href'].split('=')[1])
        if cur_page < total_page:
            next_page_url = response.url.split('=')[0] + '=' + str(cur_page + 1)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_page(self, response):
        soup = bs(response.body, 'lxml')
        title = soup.select('.topich1 h1')[0].text.strip()
        date = soup.select('.reporter time')[0]['datetime'].split()[0]
        date = date.replace('/', '-')
        cat = soup.select('.page_index li')[-1].text.strip()
        url = response.url
        text = '\n'.join([p.text.strip() for p in soup.select('article p')]).strip()

        yield {'title': title, 'date': date, 'url': url, 'text': text, 'cat': get_general_cat(cat)}
