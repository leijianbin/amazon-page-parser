import os

from amazon_page_parser import DetailParser

import pytest

@pytest.fixture(scope='module')
def detail_parsers():
    detail_page_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'pages', 'us', '0062796984.html')
    dp = DetailParser(text=)
    yield dp

def test_parse_title(detail_parsers):
    pass
