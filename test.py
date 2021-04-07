from main import url_extract
from main import pixel_check
from main import pixel_fire
import requests


def test_url_extraction():
    assert url_extract('csv_files/test.csv') == \
           {'314183':
                ['http://magnetic.domdex.com/ahtm?mp=12&n=4419&c=102651&b=108054&sz=300x250&s=${REFERER_URL_ENC}&id=${AUCTION_ID}&a=${PRICE_PAID}',
                 'http://servedby.flashtalking.com/imp/8/41606;1111860;201;pixel;Magnetic;MGNativeTestAddedValue/?cachebuster=${CACHEBUSTER}&url=http://b.scorecardresearch.com/p?c1=3&c2=6035050&c3=41606&c4=50126&c5=1111860&c6=&c10=1&c11=${SITEID}&c13=1x1&c16=gen&cj=1&ax_fwd=1&rn=${CACHEBUSTER}&']}


def test_pixel_check():
    test_url_storage = {'5555555':
                        ['http://www.foo.com',
                         'http://www.bar.com']}

    test_results = pixel_check(test_url_storage)
    assert test_results['Failed'] == 2
    assert test_results['OK'] == 0
    assert test_results['failed_tacticid'] == [['5555555', 'http://www.foo.com'],
                                               ['5555555', 'http://www.bar.com']]


def test_pixel_fire_success():
    s = requests.Session()
    test_url = 'http://www.google.com'
    assert pixel_fire(s, test_url) is True


def test_pixel_fire_failure():
    s = requests.Session()
    test_url = 'http://www.foo.com'
    assert pixel_fire(s, test_url) is None