# news-crawlers
A web crawler of news from a variety of content providers written with Scrapy.

## Requirements
- Python3+
- [Scrapy](https://scrapy.org/)

## Supported content providers
- [蘋果日報](http://tw.news.appledaily.com)
- [中國時報](https://www.chinatimes.com)

## Run
```shell
$ scrapy crawl CP [-a st=START_DATE] [-a ed=END_DATE] [-a out=OUTPUT_DIR]
```
### Symbol
- `CP`: The content provider. `apple` for 蘋果日報; `chinatimes` for 中國時報.
- `START_DATE`: The date of the earliest news article. Default is the date of **yesterday**.
- `END_DATE`: The date of the latest news article. Default is the date of **yesterday**.
- `OUTPUT_DIR`: The directory of the output json data. Defualt is `data`.

### Example
To crawl the 中國時報 new articles yesterday, run:
```shell
$ scrapy crawl chinatimes
```
To crawl the 蘋果日報 news articles from 2019-03-01 to 2019-03-20 , run:
```shell
$ scrapy crawl apple -a st=2019-03-01 -a ed=2019-03-20
```
The crawled news articles will be saved as an [ndjson](http://ndjson.org/) file in `data/news_[CP]_[START_DATE]_[END_DATE].ndjson`
