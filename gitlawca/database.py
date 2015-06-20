from __future__ import unicode_literals
from gitlawca.config import config
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base() #pylint: disable=invalid-name

#pylint: disable=W0232
def connect():
    creds = config('database')
    login = '{}:{}'.format(creds['username'], creds['password']) if creds['password'] else '{}'.format(creds['username'])
    engine = create_engine('mysql://{}@{}:{}/{}'.format(login, creds['host'], creds['port'], creds['database']))
    Base.metadata.bind = engine
    session = sessionmaker()
    session.configure(bind=engine)
    return session


def reset_database():
    session = connect()()
    session.execute('TRUNCATE TABLE acts;')
    print 'Database truncated. The scraper must be run to restore the database'


class Act(Base):
    __tablename__ = 'acts'
    id = Column(Integer, primary_key=True) #pylint: disable=C0103
    code = Column(String(50))
    short_title = Column(String(65000))
    long_title = Column(String(65000))
    act_date = Column(String(10))
    language = Column(String(10))
    url = Column(String(1000))
    error_downloading = Column(Boolean)
    git_commit = Column(String(40))
