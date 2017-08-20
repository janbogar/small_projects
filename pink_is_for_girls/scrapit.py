import scrapy
from scrapy.crawler import CrawlerProcess
from pink_is_for_girls import spiders
import inspect
import os

os.remove('images.jsonl')

spiderlist=[i[1] for i in inspect.getmembers(spiders, inspect.isclass)]

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_URI': 'images.jsonl'
    })

for s in spiderlist:
    process.crawl(s)

process.start()
