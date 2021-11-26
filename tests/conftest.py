import docker
import pytest
from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.tasks.files import write_file
from pybatfish.client.commands import bf_init_snapshot, bf_session, bf_set_network
from pybatfish.question import load_questions

# import itertools

# # Tell nornir where our inventory data is
nornir_path = "mpls_in_the_sdn_era/mpls_sdn_era_nornir"

# Evaluate wether running this locally or not to allow pipeline to execute
# properly and as well as local testing with docker-compose. The batfish
# initializing takes a long time to time out and completely errors out if it
# can't reach the batfish host.

# Get all containers running in our environment.
# This is a try block, as docker service won't be installed in our pipeline
# container and well resort to our exception and know were running this locally
# and connect to our batfish docker service by name.
try:
    client = docker.from_env()
    containers = client.containers.list()
    # Loop through all our container and extract the container names and create a
    # list to work with.
    container_names = [container.name for container in containers]
    # Simple python conditional to ensure we use the correct batfish host
    if "batfish" in container_names:
        bf_session.host = "localhost"
except docker.errors.DockerException:
    bf_session.host = "batfish"
####################################

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
def nr():
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
        logging={"enabled": True},
    )
    return nornir


def load_data(task):
    """Read all the data from the associated YAML files inside data_input dir.

    Add all the variables into a DATA_INPUT dictionary for the individual
    task.host.
    """

    data = task.run(
        task=load_yaml,
        file=f"{nornir_path}/data_input/{task.host.platform}/{task.host}.yml",
    )

    task.host["DATA_INPUT"] = data.result


# # def generate_full_mesh_list(task):
# #     """Loop through inventory hosts which are MPLS enabled devices.

# #     Generate a list of Loopback IP far-end addresses and add to a task_host[dict]
# #     to reference later as we deploy our full-mesh MPLS LSP Configuration.

# #     This task 100% depends on the success of "load_all_data" task.
# #     """
# #     # Create a list of devices from our inventory which are MPLS enabled.
# #     # List comprehension will be ran on each host to gather a list and access the
# #     # host loopback IP, which will be used as the far-end IP for the MPLS LSP.
# #     FULL_MESH_DEVICES = [
# #         host
# #         for host in nornir.inventory.hosts.keys()
# #         if "AS65000" in host and "RR" not in host and "P1" not in host
# #         if "P2" not in host
# #     ]
# #     # Remove the current task host out of the list. We don't need our local device in this
# #     # List as our goal is to gather data from the rest of the inventory from each device.
# #     # We wrap in a try/block as we are popping items we KNOW are not in that list (CE devices)
# #     # from our previous filtering.
# #     try:
# #         FULL_MESH_DEVICES.remove(f"{task.host}")
# #     except ValueError:
# #         pass

# #     # The only reason we are able to access some of these external data values is because
# #     # we loaded the external data in a previous task and added to the task.host['DATA_INPUT] dict.
# #     # We use some more list comprehension to extract all the interfaces from each host.
# #     all_hosts_interfaces = [
# #         nornir.inventory.hosts[device]["DATA_INPUT"]["ip_interfaces"]
# #         for device in FULL_MESH_DEVICES
# #     ]

# #     # Combine lists of lists into one list. We compile ALL interfaces from ALL devices besides
# #     # The current task host. We need this so we can now create one final list of all the actual
# #     # IP Addresses from the Loopbacks.
# #     interfaces = list(itertools.chain.from_iterable(all_hosts_interfaces))

# #     # Finally! Create a list of all the far-end system IP addresses (Loopbacks) to use as our
# #     # Far-END destination for configuring our full-mesh of MPLS LSPs from the current task.host.
# #     loopbacks = [
# #         ip.get("ip_address")
# #         for ip in interfaces
# #         if ip.get("description") == "SYSTEM_LO_IP"
# #     ]

#     # Check the task.host vars and ensure ifull_mesh key is True under the MPLS dict
#     # Take the newly created list and add it to a task.host[dictionary] for us to access in a different task.
#     if task.host.get("mpls_full_mesh"):
#         # print(task.host['mpls_full_mesh'])
#         task.host["loopbacks"] = loopbacks
#         # print(task.host["loopbacks"])


def render_configs(task):
    """Render device configuration using our Jinja2 Templates.

    Write staged config to file for preview/testing.
    """
    config = task.run(
        task=template_file,
        path=f"{nornir_path}/templates/configs/{task.host.platform}",
        template="main.j2",
    )

    task.host["staged"] = config.result

    write_file(
        task,
        filename=f"tests/network_data/mpls_sdn_era/configs/{task.host}.cfg",
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
    "AS65000_PE100",
    "AS65000_PE101",
    "AS65000_PE4",
    "AS65001_CE1",
    "AS65001_CE2",
    "AS65001_CE3",
    "AS65001_CE4",
]
