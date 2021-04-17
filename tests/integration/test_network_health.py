from conftest import snapshot_loader, network_inventory, core_routers
from pybatfish.question import bfq
import pytest
from pybatfish.client.asserts import (
    assert_no_incompatible_bgp_sessions,
    assert_no_unestablished_bgp_sessions,
)

# ######################################################################
# #   Example Configuration Compliance Checks to use within Pipeline   #
# ######################################################################

# """ We process our network configuration files with the latest snapshot
# of our network.
# TODO: 'review statements'

# - Initiate a instance of Nornir to generate all configs and create a proper
#   snapshot folder to provide Batfish via the pybatfish client.
# - BGP Assertions to ensure all peers will be established.
# - Ensure Device as3core1 and as1core1 have all sessions established, according
# to their configurations and parameters.
# - With an external network inventory, ensure each and every node has their
# bgp configuration within this particular network in the default VRF.
# - Validate all core-routers are configured to be route-reflectors.
# - Ensure all Loopback interfaces are set to MTU 1500. Here we pass in an
# external network inventory and check all interfaces across the network.
# """


# @pytest.fixture(scope="class")
# def bgp_setup_teardown():
#     """Initialize the test setup with correctly setting the snapshot
#     into memory"""
#     SNAPSHOT_PATH = "batfish-cicd/data/networks/dc-network/stable-dc-network"
#     snapshot_loader(SNAPSHOT_PATH, "stable-dc-network")
#     yield
#     # At the moment, there is no tear down necessary.


# @pytest.mark.usefixtures("bgp_setup_teardown")
# class TestBgpConfig:
#     @pytest.fixture
#     def bgp_config(self):
#         """Use the pybatfish SDK to extract Panda Data frame answer
#         to our network's BGP configuration"""

#         return bfq.bgpProcessConfiguration().answer().frame()

#     def test_parse_status(self):
#         """Validate all files in the current snapshot have been parsed
#         sucessfully"""

#         result = bfq.fileParseStatus().answer().frame()
#         for i, row in result.iterrows():
#             assert row.get("Status") == "PASSED"

#     @pytest.mark.parametrize("node", network_inventory)
#     def test_multipath_ebg_compliance(self, node):
#         """ Testing to ensure configuration compliance of eBGP Multipath """

#         conf = bfq.bgpProcessConfiguration(nodes=node).answer().frame()
#         for i, row in conf.iterrows():
#             assert row.get("Multipath_EBGP")

#     @pytest.mark.parametrize("node", network_inventory)
#     def test_multipath_ibg_compliance(self, node):
#         """ Testing to ensure configuration compliance of iBGP Multipath """

#         conf = bfq.bgpProcessConfiguration(nodes=node).answer().frame()
#         for i, row in conf.iterrows():
#             assert row.get("Multipath_IBGP")

#     established_nodes = [("as3core1", "ESTABLISHED"), ("as1core1", "ESTABLISHED")]

#     @pytest.mark.parametrize("node, status", established_nodes)
#     def test_bgp_state_as2core_routers(self, node, status):
#         """Testing to ensure BGP Sessions are in an Established state.
#         This is only testing against as3core1 and as1core1. The reason
#         is because we know for sure these two routers have all
#         sessions 'established'"""

#         bgp_sess_status = bfq.bgpSessionStatus(nodes=node).answer().frame()
#         for i, row in bgp_sess_status.iterrows():
#             assert row.get("Established_Status") == status

#     @pytest.mark.parametrize("node", network_inventory)
#     def test_default_vrf(self, node):
#         """Testing to ensure configuration compliance of all
#         BGP configurations are under the default VRF."""

#         conf = bfq.bgpProcessConfiguration(nodes=node).answer().frame()
#         for i, row in conf.iterrows():
#             assert row.get("VRF") == "default"

#     @pytest.mark.parametrize("node", core_routers)
#     def test_core_is_rr(self, node):
#         """Testing to ensure configuration compliance against core routers.
#         These devices must always be BGP route-reflectors.
#         Our test is only checking against devices from our inventory
#         belonging to the 'core_routers' group."""

#         conf = bfq.bgpProcessConfiguration(nodes=node).answer().frame()
#         for i, row in conf.iterrows():
#             assert row.get("Route_Reflector")

#     @pytest.mark.parametrize("node", network_inventory)
#     def test_interface_mtu(self, node):
#         """Testing to ensure network standards on MTU for x-type of interfaces.
#         This could be helpful, to ensure OSPF compliance on interfaces which are
#         expected to have neighborships. Interface Properties Question returns a
#         lot of different information on single or all interfaces in the network.
#         """

#         mtu = (
#             bfq.interfaceProperties(nodes=node, interfaces="/Loop/", properties="MTU")
#             .answer()
#             .frame()
#         )
#         for i, row in mtu.iterrows():
#             assert row.get("MTU") == 1500

#     def test_assert_no_incompatible_bgp_session(self):
#         """Built in assertion to ensure there are no incompatible BGP sessions.
#         This looks at the BGP Configuration between all nodes."""

#         assert_no_incompatible_bgp_sessions(snapshot="stable-dc-network")

#     def test_assert_no_unestablished_bgp_session(self):
#         """Assert there are no unestablished bgp sessions in our network. """

#         assert_no_unestablished_bgp_sessions(snapshot="stable-dc-network")

#     def test_undefined_refs(self):
#         """Returns nodes with structures such as ACLs, routemaps, etc. that are
#         defined but not used.
#         Or it could be harmless extra configuration generated from a master
#         template that is not meant to be used on those nodes."""

#         bfq.undefinedReferences().answer().frame()
