# -*- coding: utf-8 -*-

import json

# convert the dumped data into a real json file
def jsonfy(in_path, out_path):
    with open(in_path, 'r') as fp:
        outfile = open(out_path, 'w')
        outfile.write('[')
        for i, line in enumerate(fp):
            if i>0:
                outfile.write(',')
            outfile.write(line.strip())
        outfile.write(']')
        outfile.close()

# save crawled data to json
class NewsCrawlerPipeline(object):
    def open_spider(self, spider):
        self.fp = open(spider.lines_path, 'w')

    def process_item(self, item, spider):
        line = json.dumps(item, ensure_ascii=False) + '\n'
        self.fp.write(line)
        return item

    def close_spider(self, spider):
        self.fp.close()
        #jsonfy(spider.lines_path, spider.post_path)

