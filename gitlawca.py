from __future__ import unicode_literals
import sys
import getopt
from gitlawca.database import reset_database
from gitlawca.scrape import run as run_scraper
from gitlawca.downloader import start as run_downloader
from gitlawca.gitlawhub import reset_git_repo
from gitlawca.config import config
from git import Repo


def usage():
    print 'gitlawca command line usage'
    print ''
    print 'python gitlawca.py (-h | --help) | --reset=level | --nuke | --scrape | --download'
    print ''
    print '-h | --help: Print this message'
    print '--reset=level: --reset=database: reset Acts database, --reset=github: reset github repository, --reset=all: reset both'
    print '--nuke: Same as --reset=all'
    print '--scrape: Start scraping federal government Justice department web site for consolidated acts'
    print '--download: Start downloading and committing to Github consolidated acts in need of downloading'


def reset(arg):
    repo = Repo(config('download')['folder'])
    root_sha = config('github')['root_sha']
    if arg == 'database':
        reset_database()
    elif arg == 'github':
        reset_git_repo(repo, root_sha)
    elif arg == 'all':
        reset_database()
        reset_git_repo(repo, root_sha)
    else:
        usage()
        sys.exit()


def scrape():
    run_scraper()


def download():
    run_downloader()


def main(argv):
    try:
        opts, _ = getopt.getopt(argv, 'h', ['reset=', 'nuke', 'scrape', 'download'])
    except getopt.GetoptError:
        usage()
        sys.exit()
    if len(opts) == 0:
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt == '--reset':
            reset(arg)
        elif opt == '--nuke':
            reset('all')
        elif opt == '--scrape':
            scrape()
        elif opt == '--download':
            download()
        else:
            usage()
            sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])
