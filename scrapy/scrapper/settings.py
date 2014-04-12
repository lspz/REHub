# Scrapy settings for scrapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
import os
import random

def init_django():
  sys.path.append('../django')
  os.environ['DJANGO_SETTINGS_MODULE'] = 'rescrap.settings'
  print 'Loaded Django module..'

def init_proxy():
  proxies = [
    '208.110.67.122:7808', #oz
    '202.43.188.15:8080',
    '118.97.95.174:80',
    '202.173.222.43:8080', #thai
    '203.172.198.75:3128',
    '118.174.149.118:8080',
    '118.97.147.219:8080', #ind
    '118.98.35.251:8080'
  ]
  proxy_index = random.randrange(0, len(proxies)-1, 1)
  os.environ['http_proxy'] = proxies[proxy_index]
  print 'Using proxy: #' + str(proxy_index) + ' ' + os.environ['http_proxy']

def get_user_agent():
  agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
  ]
  return agents[random.randrange(0, len(agents)-1, 1)]

##############################

init_django()
init_proxy()

BOT_NAME = 'scrapper'

SPIDER_MODULES = ['scrapper.spiders']
NEWSPIDER_MODULE = 'scrapper.spiders'

USER_AGENT = get_user_agent()

ITEM_PIPELINES = {
  'scrapper.pipelines.DataSavePipeline': 100 # Start lower first
}

DOWNLOAD_DELAY = 0.5

DOWNLOADER_MIDDLEWARES = {
  'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 100,
}

LOG_LEVEL = 'DEBUG'#

##############################

#huh? this doesn't apply on all. make this overidable
DELETE_ON_CRAWL = False
PAGE_LIMIT = 3
DATE_ORDER_NEWEST = True 
