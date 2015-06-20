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


class ActBranch(object):

    def __init__(self, repo, branch_name):
        self.branch_name = branch_name
        self.repo = repo

    def __enter__(self):
        # Force hard reset and checkout master branch, just in case we weren't there
        self.repo.git.reset('--hard')
        self.repo.heads.master.checkout()

        branch = self.repo.create_head(self.branch_name)
        branch.checkout()
        return branch

    def __exit__(self, _, value, __):
        if value is None:
            self.repo.remote('origin').push(self.branch_name)
            return True
