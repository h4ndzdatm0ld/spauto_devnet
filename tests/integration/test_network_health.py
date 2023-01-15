import os

import pytest
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_forwarding_loops,
    assert_no_incompatible_bgp_sessions,
    assert_no_undefined_references,
    assert_no_unestablished_bgp_sessions,
)
from pybatfish.client.commands import bf_upload_diagnostics
from pybatfish.question import bfq

from tests.conftest import devices, load_data, render_configs

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

CE_DEVICES = ["AS65001_CE2", "AS65001_CE1"]


@pytest.mark.parametrize("node", devices)
def test_load_yaml(nr, node):
    """Assert all devices exist in the loaded yaml keys."""
    data = nr.run(task=load_data)
    assert node in data.keys()


@pytest.mark.parametrize("node", devices)
def test_config_gen(nr, node):
    """Render J2 Templates/Configs."""
    nr.run(task=render_configs)
    configs_dir = "tests/network_data/mpls_sdn_era/configs"
    files = os.listdir(configs_dir)
    assert f"{node}.cfg" in files


def test_assert_no_incompatible_bgp_session(snapshot_name):
    """Built in assertion to ensure there are no incompatible BGP sessions.
    This looks at the BGP Configuration between all nodes."""
    assert_no_incompatible_bgp_sessions(snapshot=snapshot_name)


def test_assert_no_unestablished_bgp_session(snapshot_name):
    """Assert there are no unestablished bgp sessions in our network."""
    assert_no_unestablished_bgp_sessions(snapshot=snapshot_name)


def test_parse_status():
    """Validate all files in the current snapshot have been parsed
    successfully. If a file is parsed but partially unrecognized,
    upload diagnostics and skip it. Unfortunately, not always does
    batfish recognize a full config correctly."""
    result = bfq.fileParseStatus().answer().frame()
    for i, row in result.iterrows():
        if row.get("Status") == "PARTIALLY_UNRECOGNIZED":
            bf_upload_diagnostics()
        else:
            assert row.get("Status") == "PASSED"


def test_unused_structures():
    """This tests checks if configuration lines are not used such as ACLs
    or route-maps"""
    result = bfq.unusedStructures().answer().frame()
    assert len(result) == 0


@pytest.mark.parametrize("node", ["AS65000_RR1", "AS65000_RR2"])
def test_rr(node):
    """Testing to ensure configuration compliance against route reflectors."""
    conf = bfq.bgpProcessConfiguration(nodes=node).answer().frame()
    for i, row in conf.iterrows():
        assert row.get("Route_Reflector")


def test_no_duplicate_routerids():
    """Built in assertion, validate router-ids."""
    assert assert_no_duplicate_router_ids()


def test_no_fw_loops():
    """ "Built in assertion, no forwarding loops"""
    assert assert_no_forwarding_loops()


def test_no_undefined_ref():
    """Validate no unused ref, such as route-maps are present, but unused."""
    assert assert_no_undefined_references()


@pytest.mark.parametrize("node", devices)
def test_bgp_state_routers(node):
    """Testing to ensure BGP Sessions are in an Established state."""
    bgp_sess_status = bfq.bgpSessionStatus(nodes=node).answer().frame()
    for i, row in bgp_sess_status.iterrows():
        assert row.get("Established_Status") == "ESTABLISHED"


# @pytest.mark.parametrize("node", CE_DEVICES)
# def test_interface_vrrp(node):
#     """Testing to ensure our CE Devices have at least 1 VRRP group, as expected."""
#     vrrp = (
#         bfq.interfaceProperties(
#             nodes=node,
#             interfaces="GigabitEthernet1.1001",
#             properties="VRRP_Groups",
#         )
#         .answer()
#         .frame()
#     )
#     for i, row in vrrp.iterrows():
#         print(row.get("Vrrp"))
#         print(row.get(len("VRRP_Groups")))
#     breakpoint()
