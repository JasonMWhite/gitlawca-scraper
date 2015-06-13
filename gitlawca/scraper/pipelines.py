from __future__ import unicode_literals
from gitlawca.database import connect
from gitlawca.database import Act


class LawscraperPipeline(object):
    def __init__(self):
        self.session = None

    def process_item(self, item, _):
        session = self.session()
        act = Act(code=item.get('code'), short_title=item.get('short_title'),
                  long_title=item.get('long_title'), act_date=item.get('act_date'),
                  language=item.get('language'), url=item.get('url'))
        session.add(act)
        session.commit()

    def open_spider(self, _):
        self.session = connect()
