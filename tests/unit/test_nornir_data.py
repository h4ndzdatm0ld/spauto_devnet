import os


class TestNornir(object):
    # Assert our network directory folder exists.
    def test_directory_configs(self):
        assert os.path.exists("tests/network_data/mpls_sdn_era/ASN65000/configs/")
