from __future__ import unicode_literals
from github import Github, GithubException
from gitlawca.config import config


def reset_git_repo(repo, root_sha):
    repo.git.reset('--hard')
    repo.heads.master.checkout()
    repo.git.reset('--hard', root_sha)
    repo.remote('origin').push(force=True)
    print 'Github repository reset to {}'.format(root_sha)


class ActBranch(object):

    def __init__(self, repo, branch_name):
        self.branch_name = branch_name
        self.repo = repo
        self.branch = None
        git_config = config('github')
        self.username = git_config['user']
        self.github_token = git_config['token']
        self.github_repo_name = git_config['repo']

    def __enter__(self):
        # Force hard reset and checkout master branch, just in case we weren't there
        self.repo.git.reset('--hard')
        self.repo.git.clean('-f', '-d')
        self.repo.heads.master.checkout()

        self.branch = self.repo.create_head(self.branch_name)
        self.branch.checkout()
        return self.branch

    def _push_to_github(self):
        try:
            self.repo.remote('origin').push(self.branch_name)
            github_access = Github(self.github_token)
            github_repo = github_access.get_repo("{}/{}".format(self.username, self.github_repo_name))
            pull = github_repo.create_pull(title="Merging acts from {}".format(self.branch_name), body="Merging acts from {}".format(self.branch_name), base=self.repo.heads.master.name, head=self.branch.name)
            pull.merge()
            self.repo.remote('origin').push(['--delete', self.branch_name])
        except GithubException as ex:
            print 'Unsuccessful merge: {}'.format(str(ex.data))


    def __exit__(self, _, value, __):
        if value is None:
            self._push_to_github()
        else:
            self.repo.git.reset('--hard')
            self.repo.git.clean('-f', '-d')

        self.repo.heads.master.checkout()
        self.repo.git.branch('-D', self.branch_name)
