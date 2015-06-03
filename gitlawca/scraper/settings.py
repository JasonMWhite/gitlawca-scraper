# -*- coding: utf-8 -*-

# Scrapy settings for lawscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'gitlaw-scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lawscraper (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'gitlawca.scraper.pipelines.LawscraperPipeline': 100
}
