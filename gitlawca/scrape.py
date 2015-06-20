from gitlawca.scraper.spiders.canada_law import CanadaLawSpider
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings

#pylint: disable=no-member
def spider_closing():
    """Activates on spider closed signal"""
    log.msg("Closing reactor", level=log.INFO)
    reactor.stop()


def run():
    log.start(loglevel=log.DEBUG)
    settings = Settings()

    # crawl responsibly
    settings.set("USER_AGENT", "Gitlaw-ca Scraper (+https://github.com/JasonMWhite/gitlawca-scraper)")
    settings.set("ITEM_PIPELINES", {'gitlawca.scraper.pipelines.LawscraperPipeline': 100})
    crawler = Crawler(settings)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)

    crawler.configure()
    crawler.crawl(CanadaLawSpider())
    crawler.start()
    reactor.run()
