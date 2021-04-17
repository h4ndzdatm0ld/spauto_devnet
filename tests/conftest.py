from pybatfish.client.commands import (
    bf_init_snapshot,
    bf_set_network,
    bf_session,
)
from pybatfish.question import load_questions
from nornir import InitNornir
from nornir.core.state import GlobalState
import pytest

# Identify where the Batfish service is running
bf_session.host = "batfish"  # when running in compose
# Tell batfish which network we are working with
bf_set_network("dc-network")
# Load Questions
load_questions()


def snapshot_loader(snap_path, name, overwrite=True):
    """Simple function to load a snapshot into Batfish. This function allows
    up to use a setup fixture and extend to multiple test cases against
    different snapshots of the network."""

    bf_init_snapshot(snap_path, name=name, overwrite=overwrite)


global_data = GlobalState(dry_run=True)


@pytest.fixture(scope="session", autouse=True)
def nr(request):
    """Initializes Nornir."""

    # Tell nornir where our inventory data is
    nornir_path = "mpls_in_the_sdn_era/mpls_sdn_era_nornir/inventory"

    nornir = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{nornir_path}/hosts.yml",
                "group_file": f"{nornir_path}/groups.yml",
                "defaults_file": f"{nornir_path}/defaults.yml",
            },
        },
        dry_run=True,
    )
    nornir.data = global_data
    return nornir


@pytest.fixture(scope="function", autouse=True)
def reset_data():
    global_data.dry_run = True
    global_data.reset_failed_hosts()
