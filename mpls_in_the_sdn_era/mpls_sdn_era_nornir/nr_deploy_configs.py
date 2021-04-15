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

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")


def assert_data():
    """Error checking of input data."""
    pass
    # Add schema enforcer
    # However, assert simple things like ip addresses, etc


def load_all_data(task):
    """Read all the data from the assosciated YAML files inside data_input dir.

    Add all the variables into a DATA_INPUT dictionary for the individual
    task.host.
    """
    data = task.run(
        task=load_yaml, file=f"data_input/{task.host.platform}/{task.host}.yml"
    )
    task.host["DATA_INPUT"] = data.result


def render_main(task):
    """Render device configuration using our Jinja2 Templates.

    Write staged config to file for preview/debugging.
    """
    config = task.run(
        task=template_file,
        path="templates/configs",
        template="main.j2",
    )

    task.host["staged"] = config.result

    asn = task.host["asn"]
    write_file(
        task,
        filename=f"staged/configs/ASN{asn}/{task.host}.cfg",
        content=f"{task.host['staged']}",
    )


def push_config(task):
    """Push configurations to devices."""
    task.run(
        netmiko_send_config, config_commands=f"{task.host['staged']}", cmd_verify=False
    )
    task.run(netmiko_commit)


def main():
    """Execute our Nornir runbook."""
    nr.run(task=load_all_data)
    print_result(nr.run(task=render_main))
    print_result(nr.run(task=push_config))


if __name__ == "__main__":
    main()
