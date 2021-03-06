from __future__ import unicode_literals
from gitlawca.config import config
from gitlawca.database import connect, Act
from sqlalchemy import func
from gitlawca.gitlawhub import ActBranch
from git import Repo
import os.path
import urllib2
from gitlawca.law_parser import prepare_markdown
from time import sleep

#pylint: disable=W0511

download_config = config('download')


def act_file_location(act):
    act_prefix = act.code.split('-')[0]
    return os.path.join('canada', act.language, 'acts', act_prefix, act.code + '.md')


def determine_next_commit_date(session):
    next_date = session.query(func.min(Act.act_date).label('min_date')).filter(Act.git_commit.is_(None)).first()
    if next_date is not None:
        next_date = next_date.min_date
    return next_date


def get_acts_by_date(session, act_date):
    return session.query(Act).filter(Act.git_commit.is_(None)).filter(Act.act_date == act_date).all()[0:download_config['limit']]


def start():
    session = connect()()
    try:
        next_date_to_download = determine_next_commit_date(session)
        if next_date_to_download is None:
            return

        repo = Repo(download_config['folder'])
        os.chdir(download_config['folder'])

        with ActBranch(repo, next_date_to_download) as branch:
            acts = get_acts_by_date(session, next_date_to_download)
            print 'Found {} acts to download'.format(len(acts))

            for act in acts:
                filename = act_file_location(act)

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                text = download_act(act)

                if text is None:
                    continue

                text = unicode(text, 'utf8')
                text = prepare_markdown(text)

                with open(filename, 'w') as f:
                    f.write(text.encode('utf8', 'replace'))
                repo.index.add([filename])

            repo.index.commit("Acts modified on {}".format(next_date_to_download))

            for act in acts:
                act.git_commit = branch.commit.hexsha

            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def download_act(act):
    max_retries = config('download')['retries']

    num_retries = 0
    text = None
    print 'Downloading file from {}'.format(act.url)
    while text is None and num_retries < max_retries:
        try:
            doc = urllib2.urlopen(act.url)
            text = doc.read()
        except urllib2.URLError:
            sleep(1)
            num_retries += 1

    if text is None:
        print 'Error downloading file from {}'.format(act.url)
        act.error_downloading = True
    return text
