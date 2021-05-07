"""Example NETCONF Python Script."""

# from ncclient import manager

# # Create an XML filter for targeted NETCONF queries
# netconf_filter = """
# <filter>
#     <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
#         <interface></interface>
#     </interfaces>
# </filter>"""

# with manager.connect(
#     host="192.168.0.173",
#     port=830,
#     username="admin",
#     password="admin",
#     look_for_keys=False,
#     hostkey_verify=False,
#     device_params={"name": "iosxr"},
# # ) as m:

#     netconf_reply = m.get_config(source="running")
#     print(netconf_reply)
