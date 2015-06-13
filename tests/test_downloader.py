from __future__ import unicode_literals
from downloader import Downloader
from gitlawca.database import Act
import pytest

#pylint: disable=R0201
class TestDownloader(object):

    @pytest.fixture
    def dl(self):
        dl = Downloader()
        dl.root_folder = '~/data'
        return dl

    @pytest.fixture
    def act(self):
        act = Act()
        act.code = 'A-1'
        act.act_date = '20150101'
        act.language = 'eng'
        return act

    def test_act_file_location(self, dl, act):
        assert dl.act_file_location(act) == '~/data/canada/acts/A-1/eng/20150101.html'
