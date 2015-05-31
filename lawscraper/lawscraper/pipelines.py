from __future__ import unicode_literals
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#pylint: disable=W0232

Base = declarative_base() #pylint: disable=invalid-name

class Act(Base):
    __tablename__ = 'acts'
    id = Column(Integer, primary_key=True), #pylint: disable=C0103
    code = Column(String(50))
    short_title = Column(String(65000))
    long_title = Column(String(65000))
    act_date = Column(String(10))
    language = Column(String(10))


class LawscraperPipeline(object):
    def __init__(self):
        self.session = None

    def process_item(self, item, _):
        session = self.session()
        act = Act(code=item.get('code'), short_title=item.get('short_title'),
                  long_title=item.get('long_title'), act_date=item.get('act_date'),
                  language=item.get('language'))
        session.add(act)
        session.commit()

    def open_spider(self, _):
        engine = create_engine('mysql://root@shop.myshopify.io/gitlawca')
        Base.metadata.bind = engine
        self.session = sessionmaker()
        self.session.configure(bind=engine)
