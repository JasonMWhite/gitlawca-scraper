from __future__ import unicode_literals
from gitlawca.config import config
from gitlawca.database import connect, Act
import os.path
import urllib2


class Downloader(object):

    def __init__(self):
        self.root_folder = config('download_folder')

    def start_download(self):
        # TODO: better session logic, see http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
        session = connect()()
        try:
            files_to_download = self.get_files_to_download(session)
        except:
            session.rollback()
            raise
        finally:
            session.close()

        print 'Found {} files to download'.format(len(files_to_download))

        for (act, filename) in files_to_download:
            self.download_file(act, filename)

    def get_files_to_download(self, session):
        files_to_download = []
        for act in session.query(Act):
            filename = self.act_file_location(act)
            if not os.path.exists(filename):
                files_to_download.append((act, filename))
        return files_to_download

    def act_file_location(self, act):
        return os.path.join(self.root_folder, 'canada', 'acts', act.code, act.language, act.act_date + '.html')

    def download_file(self, act, filename):
        #TODO: read whole file before writing
        if not os.path.exists(os.path.dirname(filename)):
            print 'Creating folder to store files'
            os.makedirs(os.path.dirname(filename))

        try:
            text = urllib2.urlopen(act.url)
            print 'Downloading file from {}'.format(act.url)
            with open(filename, 'w') as file:
                file.write(text.read())
            print 'Saved file to {}'.format(filename)
        except urllib2.HTTPError:
            #TODO: don't use sessions this way
            session = connect()()
            session.add(act)
            act.error_downloading = True
            session.commit()
            session.close()

d = Downloader()
d.start_download()
