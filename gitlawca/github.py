from __future__ import unicode_literals
from gitlawca.config import config
from git import Repo


def reset_git_repo():
    root_sha = config('github')['root_sha']
    repo = Repo(config('download_folder'))
    repo.git.reset('--hard')
    repo.heads.master.checkout()
    repo.git.reset('--hard', root_sha)
    repo.remote('origin').push(force=True)
    print 'Github repository reset to {}'.format(root_sha)
