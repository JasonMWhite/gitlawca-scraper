from __future__ import unicode_literals

import pytest
from gitlawca import downloader
from gitlawca.database import Act

#pylint: disable=W0621
@pytest.fixture
def act():
    output = Act()
    output.code = 'A-1'
    output.act_date = '20150101'
    output.language = 'eng'
    return output

def test_act_file_location(act):
    assert downloader.act_file_location(act) == 'canada/acts/eng/A/A-1.md'
