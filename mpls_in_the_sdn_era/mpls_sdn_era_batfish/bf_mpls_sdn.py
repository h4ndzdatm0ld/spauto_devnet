from pybatfish.client.commands import bf_upload_diagnostics
from pybatfish.question import bfq
from pybatfish.client.asserts import (
    assert_no_incompatible_bgp_sessions,
    assert_no_unestablished_bgp_sessions,
    assert_no_duplicate_router_ids,
    assert_no_forwarding_loops,
    assert_no_undefined_references,
)

# TODO: Make sure to simply run pytest and generate the latest configs using Nornir
CONFIGS = "../tests/network_data/mpls_sdn_era/ASN65000/configs"
