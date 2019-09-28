# news-crawlers
A web crawler of news from a variety of content providers written with Scrapy.

## Requirements
- Python3+
- [Scrapy](https://scrapy.org/)

## Supported content providers
- ~~[蘋果日報](http://tw.news.appledaily.com)~~(改成會員制)
- [中國時報](https://www.chinatimes.com)
- [自由時報](https://www.ltn.com.tw/)
- [聯合新聞網](https://udn.com)

## Run
```shell
$ scrapy crawl CP [-a out=OUTPUT_DIR]
```
### Symbol
- `CP`: The content provider. `chinatimes` for 中國時報; `ltn` for 自由時報; `udn` for 聯合新聞網.
- `OUTPUT_DIR`: The directory of the output json data. Defualt is `data`.

### Example
To crawl the 自由時報 real-time new articles, run:
```shell
$ scrapy crawl ltn
```

The crawled news articles will be saved as an [ndjson](http://ndjson.org/) file in `data/news_[CP]_[%Y%m%dT%H%M].ndjson`
