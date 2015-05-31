# -*- coding: utf-8 -*-

# Scrapy settings for lawscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'lawscraper'

SPIDER_MODULES = ['lawscraper.spiders']
NEWSPIDER_MODULE = 'lawscraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lawscraper (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'lawscraper.lawscraper.pipelines.LawscraperPipeline': 100
}
