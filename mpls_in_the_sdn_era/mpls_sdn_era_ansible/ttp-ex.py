from ttp import ttp

data_to_parse = """
router bgp 65001
 bgp router-id 192.168.10.1
 bgp log-neighbor-changes
 neighbor 10.1.0.1 remote-as 65000
 neighbor 10.1.0.1 update-source GigabitEthernet2.1001
 neighbor 10.1.0.5 remote-as 65000
 neighbor 10.1.0.5 update-source GigabitEthernet3.1001
 !
 address-family ipv4
  redistribute connected
  neighbor 10.1.0.1 activate
  neighbor 10.1.0.1 send-community both
  neighbor 10.1.0.1 route-map PL-EBGP-PE1-OUT out
  neighbor 10.1.0.5 activate
  neighbor 10.1.0.5 send-community both
  neighbor 10.1.0.5 route-map PL-EBGP-PE2-OUT out
 exit-address-family
"""

ttp_template = """
<macro>
def to_bool(captured_data):
    represent_as_bools = ["activate", "log-neighbor-changes"]
    if captured_data in represent_as_bools:
        return captured_data, {captured_data: True}
</macro>

<group name="bgp">
router bgp {{ asn }}
 bgp router-id {{ router-id }}
 bgp {{ log-neighbor-changes | macro('to_bool')}}
 <group name="neighbor.{{ neighbor }}">
 neighbor {{ neighbor }} remote-as {{ remote-as }}
 neighbor 10.1.0.1 update-source {{ update-source }}
 </group>
 ! {{ ignore }}
 <group name="afi.{{ afi }}">
 address-family {{ afi }}
  redistribute {{ redistribute }}
  <extend template="templates/bgp_neighbors.txt"/>
 exit-address-family {{ ignore }}
 </group>
</group>
"""

# create parser object and parse data using template:
parser = ttp(data=data_to_parse, template=ttp_template)
parser.parse()

# print result in JSON format
results = parser.result(format='json')[0]
print(results)
