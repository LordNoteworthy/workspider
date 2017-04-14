# -*- coding: utf-8 -*-

# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

ITEM_PIPELINES = {
    'scraper.pipelines.JobsPipeline': 300
}


DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'scraper.comm.rotate_useragent.RotateUserAgentMiddleware': 400
    }

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'workspider_user',
            'password': 'workspider_pass',
            'database': 'workspider_db'}

LOG_LEVEL = 'DEBUG'
DOWNLOAD_DELAY = 0.5
COOKIES_ENABLED = True
