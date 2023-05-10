import os

import pytest
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_forwarding_loops,
    assert_no_incompatible_bgp_sessions,
    assert_no_undefined_references,
    assert_no_unestablished_bgp_sessions,
)

from tests.conftest import CONFIGS_DIR, devices, load_data, render_configs

# # ######################################################################
# # #   Example Configuration Compliance Checks to use within Pipeline   #
# # ######################################################################

""" We process our network configuration files with the latest snapshot
of our network.

- Initiate a instance of Nornir to generate all configs and create a proper
snapshot folder to provide Batfish via the pybatfish client.
- BGP Assertions to ensure all peers will be established.
- Validate all core-routers are configured to be route-reflectors.
- Validate BGP is healthy, no unestablished peers, etc.
- Validate no undefined references.
- Validate no duplicate router-ids.
"""

CE_DEVICES = ["AS65001_CE2", "AS65001_CE1", "AS65001_CE3", "AS65001_CE4"]
ALL_NETWORK_DEVICES = devices()


@pytest.mark.parametrize("node", ALL_NETWORK_DEVICES)
def test_load_yaml(nr, node):
    """Assert all devices exist in the loaded yaml keys."""
    data = nr.run(task=load_data)
    assert node in data.keys()


@pytest.mark.parametrize("node", ALL_NETWORK_DEVICES)
def test_config_gen(nr, node):
    """Render J2 Templates/Configs."""
    nr.run(task=load_data)
    result = nr.run(task=render_configs)
    assert node in result.keys()


@pytest.mark.parametrize("node", ALL_NETWORK_DEVICES)
def test_config_gen_output(nr, node):
    """Render J2 Templates/Configs."""
    files = os.listdir(CONFIGS_DIR)
    # Default Config, nothing to render/install.
    if not node == "AS65001_SW_01":
        assert f"{node}.cfg" in files


@pytest.mark.usefixtures("batfish_session")
def test_assert_no_incompatible_bgp_session(batfish_session, snapshot_name):
    """Built in assertion to ensure there are no incompatible BGP sessions.

    This looks at the BGP Configuration between all nodes."""
    assert_no_incompatible_bgp_sessions(snapshot=snapshot_name, session=batfish_session)


@pytest.mark.usefixtures("batfish_session")
def test_assert_no_unestablished_bgp_session(batfish_session, snapshot_name):
    """Assert there are no unestablished bgp sessions in our network."""
    assert_no_unestablished_bgp_sessions(
        snapshot=snapshot_name, session=batfish_session
    )


@pytest.mark.usefixtures("batfish_session")
def test_parse_status(batfish_session):
    """Validate all files in the current snapshot have been parsed
    successfully. If a file is parsed but partially unrecognized,
    upload diagnostics and skip it. Unfortunately, not always does
    batfish recognize a full config correctly."""
    result = batfish_session.q.fileParseStatus().answer().frame()
    for i, row in result.iterrows():
        if not row.get("File_format") == "CISCO_IOS":
            continue
        assert row.get("Status") == "PASSED"


@pytest.mark.usefixtures("batfish_session")
def test_unused_structures(batfish_session):
    """This tests checks if configuration lines are not used such as ACLs
    or route-maps"""
    result = batfish_session.q.unusedStructures().answer().frame()
    assert len(result) == 0


@pytest.mark.usefixtures("batfish_session")
@pytest.mark.parametrize("node", ["AS65000_RR1", "AS65000_RR2"])
def test_rr(batfish_session, node):
    """Testing to ensure configuration compliance against route reflectors."""
    conf = batfish_session.q.bgpProcessConfiguration(nodes=node).answer().frame()
    for i, row in conf.iterrows():
        assert row.get("Route_Reflector")


@pytest.mark.usefixtures("batfish_session")
def test_no_duplicate_routerids(snapshot_name, batfish_session):
    """Built in assertion, validate router-ids."""
    assert assert_no_duplicate_router_ids(
        snapshot=snapshot_name, session=batfish_session
    )


@pytest.mark.usefixtures("batfish_session")
def test_no_fw_loops(batfish_session, snapshot_name):
    """ "Built in assertion, no forwarding loops"""
    assert assert_no_forwarding_loops(session=batfish_session, snapshot=snapshot_name)


@pytest.mark.usefixtures("batfish_session")
def test_no_undefined_ref(batfish_session, snapshot_name):
    """Validate no unused ref, such as route-maps are present, but unused."""
    assert assert_no_undefined_references(
        session=batfish_session, snapshot=snapshot_name
    )


@pytest.mark.usefixtures("batfish_session")
@pytest.mark.parametrize("node", ALL_NETWORK_DEVICES)
def test_bgp_state_routers(node, batfish_session):
    """Testing to ensure BGP Sessions are in an Established state."""
    bgp_sess_status = batfish_session.q.bgpSessionStatus(nodes=node).answer().frame()
    for i, row in bgp_sess_status.iterrows():
        assert row.get("Established_Status") == "ESTABLISHED"
