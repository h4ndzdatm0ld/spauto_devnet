from nornir import InitNornir
import pytest
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.files import write_file

from pybatfish.client.commands import (
    bf_init_snapshot,
    bf_set_network,
    bf_session,
)
from pybatfish.question import load_questions


# # Tell nornir where our inventory data is
nornir_path = "mpls_in_the_sdn_era/mpls_sdn_era_nornir"

# Identify where the Batfish service is running
bf_session.host = "localhost"  # when running in compose
# Tell batfish which network we are working with
bf_set_network("mpls_sdn_era")
# Load Questions
load_questions()


def snapshot_loader(snap_path, name, overwrite=True):
    """Simple function to load a snapshot into Batfish. This function allows
    up to use a setup fixture and extend to multiple test cases against
    different snapshots of the network."""

    bf_init_snapshot(snap_path, name=name, overwrite=overwrite)


@pytest.fixture(scope="class", autouse=True)
def nornir():
    """Initializes Nornir. Disable Logging to avoid pytest warnings."""

    nornir = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{nornir_path}/inventory/hosts.yml",
                "group_file": f"{nornir_path}/inventory/groups.yml",
                "defaults_file": f"{nornir_path}/inventory/defaults.yml",
            },
        },
        logging={"enabled": False},
    )
    return nornir


def load_data(task):
    """Read all the data from the assosciated YAML files inside data_input dir.

    Add all the variables into a DATA_INPUT dictionary for the individual
    task.host.
    """

    data = task.run(
        task=load_yaml,
        file=f"{nornir_path}/data_input/{task.host.platform}/{task.host}.yml",
    )

    task.host["DATA_INPUT"] = data.result


def render_configs(task):
    """Render device configuration using our Jinja2 Templates.

    Write staged config to file for preview/testing.
    """
    config = task.run(
        task=template_file,
        path=f"{nornir_path}/templates/configs",
        template="main.j2",
    )

    task.host["staged"] = config.result

    asn = task.host["asn"]
    write_file(
        task,
        filename=f"tests/network_data/mpls_sdn_era/ASN{asn}/configs/{task.host}.cfg",
        content=f"{task.host['staged']}",
    )


devices = [
    "AS65000_P1",
    "AS65000_P2",
    "AS65000_RR1",
    "AS65000_RR2",
    "AS65000_PE1",
    "AS65000_PE2",
    "AS65000_PE3",
    "AS65000_PE4",
]
