# -*- coding: utf-8 -*-

import json
import os

# save crawled data to ndjson
class NewsCrawlerPipeline(object):

    def open_spider(self, spider):
        if not os.path.exists(spider.directory):
            os.makedirs(spider.directory)
        self.fp = open(os.path.join(spider.directory, spider.file), 'w')

    def process_item(self, item, spider):
        line = json.dumps(item, ensure_ascii=False) + '\n'
        self.fp.write(line)
        return item

    def close_spider(self, spider):
        self.fp.close()

