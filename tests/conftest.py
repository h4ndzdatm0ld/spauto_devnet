import logging
from typing import List

import pytest
from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.tasks.files import write_file
from pybatfish.client.session import Session

NORNIR_PATH: str = "spauto/nornir"
BATFISH_HOST: str = "localhost"
SNAPSHOT_PATH: str = "tests/network_data/mpls_sdn_era"
CONFIGS_DIR: str = f"{SNAPSHOT_PATH}/configs/"
NETWORK_NAME: str = "mpls_sdn_era"


logging.getLogger("pybatfish").setLevel(logging.DEBUG)


@pytest.fixture(scope="session")
def snapshot_name():
    return NETWORK_NAME


def devices():
    """Network Devices."""
    network_devices: List = [
        "AS65000_P1",
        "AS65000_P2",
        "AS65000_RR1",
        "AS65000_RR2",
        "AS65000_PE1",
        "AS65000_PE2",
        "AS65000_PE3",
        "AS65000_PE4",
        "AS65001_CE1",
        "AS65001_CE2",
        "AS65001_CE3",
        "AS65001_CE4",
        "AS65001_H1",
        "AS65001_H2",
        "AS65001_SW_01",
    ]
    return network_devices


@pytest.fixture(scope="session")
def batfish_session():
    batfish = Session(host=BATFISH_HOST)
    batfish.set_network(NETWORK_NAME)
    batfish.init_snapshot(SNAPSHOT_PATH, NETWORK_NAME, overwrite=True)
    return batfish


@pytest.mark.usefixtures("batfish_session")
@pytest.fixture
def bgp_config(batfish_session):
    """Use the pybatfish SDK to extract Panda Data frame answer
    to our network's BGP configuration"""
    return batfish_session.q.bgpProcessConfiguration().answer().frame()


@pytest.fixture(scope="class", autouse=True)
def nr():
    """Initializes Nornir. Disable Logging to avoid pytest warnings."""
    nornir = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{NORNIR_PATH}/inventory/hosts.yml",
                "group_file": f"{NORNIR_PATH}/inventory/groups.yml",
                "defaults_file": f"{NORNIR_PATH}/inventory/defaults.yml",
            },
        },
        logging={"enabled": True},
    )
    return nornir


def load_data(task):
    """Read all the data from the associated YAML files inside data_input dir.

    Add all the variables into a data_input dictionary for the individual
    task.host.
    """
    data = task.run(
        task=load_yaml,
        file=f"{NORNIR_PATH}/data_input/{task.host.platform}/{task.host}.yml",
    )
    task.host["data_input"] = data.result


def render_configs(task):
    """Render device configuration using our Jinja2 Templates.

    Write staged config to file for preview/testing.
    """
    config = task.run(
        task=template_file,
        path=f"{NORNIR_PATH}/templates/configs/{task.host.platform}",
        template="main.j2",
    )

    task.host["staged"] = config.result

    write_file(
        task,
        filename=f"tests/network_data/mpls_sdn_era/configs/{task.host}.cfg",
        content=f"{task.host['staged']}",
    )
