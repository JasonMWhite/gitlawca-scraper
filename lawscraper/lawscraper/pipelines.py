# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Act(Base):
    __tablename__ = 'acts'
    id = Column(Integer, primary_key=True)
    code = Column(String(50))
    short_title = Column(String(65000))
    long_title = Column(String(65000))
    act_date = Column(String(10))
    language = Column(String(10))


class LawscraperPipeline(object):
    def process_item(self, item, spider):
        s = self.session()
        act = Act(code=item.get('code'), short_title=item.get('short_title'),
                  long_title=item.get('long_title'), act_date=item.get('act_date'),
                  language=item.get('language'))
        s.add(act)
        s.commit()

    def open_spider(self, spider):
        engine = create_engine('mysql://root@shop.myshopify.io/gitlawca')
        Base.metadata.bind = engine
        self.session = sessionmaker()
        self.session.configure(bind=engine)
