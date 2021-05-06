"""Interactive Batfish Script."""
from pybatfish.client.commands import bf_upload_diagnostics
from pybatfish.question import bfq
from pybatfish.client.asserts import (
    assert_no_incompatible_bgp_sessions,
    assert_no_unestablished_bgp_sessions,
    assert_no_duplicate_router_ids,
    assert_no_forwarding_loops,
    assert_no_undefined_references,
)
from pybatfish.question import load_questions
from pybatfish.client.commands import (
    bf_init_snapshot,
    bf_set_network,
    bf_session,
    bf_set_snapshot,
)

CONFIGS = "../../mpls_in_the_sdn_era/mpls_sdn_era_nornir/napalm_getters/mpls_sdn_era/"


def snapshot_loader(snap_path, name, overwrite=True):
    """Simple function to load a snapshot into Batfish.

    This function allows up to use a setup fixture and extend to multiple
    test cases against thedifferent snapshots of the network.
    """
    bf_init_snapshot(snap_path, name=name, overwrite=overwrite)


def main():
    """Execute Batfish Interactive."""
    bf_set_network("mpls_sdn_era")
    # Load Questions
    load_questions()

    snapshot_loader(CONFIGS, "MPLS_SDN_ERA")
    bf_set_snapshot("MPLS_SDN_ERA")

    config_process = bfq.bgpProcessConfiguration().answer().frame()
    refs = bfq.unusedStructures().answer().frame()
    parse = bfq.fileParseStatus().answer().frame()

    bfq.initIssues().answer()

main()
