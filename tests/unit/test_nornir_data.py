import os


class TestNornir(object):
    # Assert our network directory folder exists.
    def test_directory_configs_unit(self):
        assert os.path.exists("tests/network_data/mpls_sdn_era/configs/")
