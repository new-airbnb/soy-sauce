from utils import utils


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
