from utils import utils
from datetime import date


class TestUtils(object):
    def test_str_to_boolean(self):
        cases = [
            ("True", True),
            ("False", False),
            ("true", True),
            ("false", False)
        ]
        for s, gt in cases:
            assert utils.str_to_boolean(s) == gt

    def test_get_timestamp(self):
        stamp = utils.get_timestamp()
        assert stamp.endswith('Z')

    def test_get_date_timestamp(self):
        stamp = utils.get_date_timestamp(date(year=2019,month=2,day=28))
        assert stamp == '2019-02-28'
