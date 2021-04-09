#!/usr/bin/python3
from nornir import InitNornir
from nornir_netmiko.tasks import (
    netmiko_send_command,
    netmiko_send_config,
    netmiko_commit,
)
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by the 'PE' router type.
pe_routers = nr.filter(type="PE_ROUTER")


def assert_data():
    pass
    # Add schema enforcer
    # However, assert simple things like ip addresses, etc


def load_all_data(task):
    """Read all the data from the assosciated YAML files inside data_input
    folder. Add all the variables into a DATA_INPUT dictionary for the
    individual task.host."""

    data = task.run(
        task=load_yaml, file=f"data_input/{task.host.platform}/{task.host}.yml"
    )
    task.host["DATA_INPUT"] = data.result


def render_main(task):

    base = task.run(
        task=template_file,
        path="templates/configs",
        template="main.j2",
    )

    task.run(netmiko_send_config, config_commands=base.result, cmd_verify=False)
    task.run(netmiko_commit)


def main():

    nr.run(task=load_all_data)
    print_result(nr.run(task=render_main))


if __name__ == "__main__":
    main()
