#!/usr/bin/python3
"""This script will generate configurations by rendering our Jinja templates.

Configurations are deployed via Netmiko/Nornir to our devices.
Before using this script, make sure you update the inventory host file with
the correct Out of Band IP devices assigned to your lab topology.
"""
from nornir import InitNornir
from nornir_netmiko.tasks import (
    netmiko_send_config,
    netmiko_commit,
)
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.tasks.files import write_file
import itertools

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Test Filter, unused.
# full_mesh = nr.filter(mpls_full_mesh=True)


def assert_data():
    """Error checking of input data."""
    pass
    # Add schema enforcer
    # However, assert simple things like ip addresses, etc


def load_all_data(task):
    """Read all the data from the associated YAML files inside data_input dir.

    Add all the variables into a DATA_INPUT dictionary for the individual
    task.host.
    """
    data = task.run(
        task=load_yaml, file=f"data_input/{task.host.platform}/{task.host}.yml"
    )
    task.host["DATA_INPUT"] = data.result


def generate_full_mesh_list(task):
    """Loop through inventory hosts which are MPLS enabled devices.

    Generate a list of Loopback IP far-end addresses and add to a task_host[dict]
    to reference later as we deploy our full-mesh MPLS LSP Configuration.

    This task 100% depends on the success of "load_all_data" task.
    """
    # Create a list of devices from our inventory which are MPLS enabled.
    # List comprehension will be ran on each host to gather a list and access the
    # host loopback IP, which will be used as the far-end IP for the MPLS LSP.
    FULL_MESH_DEVICES = [
        host
        for host in nr.inventory.hosts.keys()
        if "AS65000" in host and "RR" not in host and "P1" not in host
        if "P2" not in host and "101" not in host and "100" not in host
    ]
    # Remove the current task host out of the list. We don't need our local device in this
    # List as our goal is to gather data from the rest of the inventory from each device.
    # We wrap in a try/block as we are popping items we KNOW are not in that list (CE devices)
    # from our previous filtering.
    try:
        FULL_MESH_DEVICES.remove(f"{task.host}")
    except ValueError:
        pass

    # The only reason we are able to access some of these external data values is because
    # we loaded the external data in a previous task and added to the task.host['DATA_INPUT] dict.
    # We use some more list comprehension to extract all the interfaces from each host.
    all_hosts_interfaces = [
        nr.inventory.hosts[device]["DATA_INPUT"]["ip_interfaces"]
        for device in FULL_MESH_DEVICES
    ]
    # Combine lists of lists into one list. We compile ALL interfaces from ALL devices besides
    # The current task host. We need this so we can now create one final list of all the actual
    # IP Addresses from the Loopbacks.
    interfaces = list(itertools.chain.from_iterable(all_hosts_interfaces))
    # Finally! Create a list of all the far-end system IP addresses (Loopbacks) to use as our
    # Far-END destination for configuring our full-mesh of MPLS LSPs from the current task.host.
    loopbacks = [
        ip.get("ip_address")
        for ip in interfaces
        if ip.get("description") == "SYSTEM_LO_IP"
    ]
    # Check the task.host vars and ensure ifull_mesh key is True under the MPLS dict
    # Take the newly created list and add it to a task.host[dictionary] for us to access in a different task.
    if task.host.get("mpls_full_mesh"):
        # print(task.host['mpls_full_mesh'])
        task.host["loopbacks"] = loopbacks
        # print(f"{task.host} : {task.host['loopbacks']}")


def render_main(task):
    """Render device configuration using our Jinja2 Templates.

    Write staged config to file for preview/debugging.
    """
    config = task.run(
        task=template_file,
        path=f"templates/configs/{task.host.platform}",
        template="main.j2",
    )

    task.host["staged"] = config.result

    write_file(
        task,
        filename=f"staged/configs/ASN{task.host.get('asn')}/{task.host}.cfg",
        content=f"{task.host['staged']}",
    )


def push_config(task):
    """Push configurations to devices."""
    if task.host.platform == "cisco_xr":
        task.run(
            netmiko_send_config,
            config_commands=f"{task.host['staged']}",
            cmd_verify=False,
        )
        task.run(netmiko_commit)
    elif task.host.platform == "cisco_xe":
        task.run(
            netmiko_send_config,
            config_commands=f"{task.host['staged']}".split("\n"),
        )
    elif task.host.platform == "cisco_ios":
        task.run(
            netmiko_send_config,
            config_commands=f"{task.host['staged']}".split("\n"),
        )


def main():
    """Execute our Nornir runbook."""
    nr.run(task=load_all_data)
    print_result(nr.run(task=generate_full_mesh_list))
    print_result(nr.run(task=render_main))
    print_result(nr.run(task=push_config))


if __name__ == "__main__":
    main()
