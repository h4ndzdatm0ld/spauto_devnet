# MPLS in the SDN Era --> DevNet SPAUTO
 Get right to the study material: [Checkout the Wiki!](https://github.com/h4ndzdatm0ld/mpls_in_the_sdn_era/wiki)

## A lab topology based on MPLS in the SDN era book used for 300-535 SPAUTO studies.
[Cisco Certified DevNet Specialist - Service Provider Automation and Programmability](https://developer.cisco.com/certification/devnet-sp-auto/)
## Why MPLS in the SDN Era?

Simple. This is an incredible book for any and all Network Engineers interested
in learning technologies used in Service Provider environments. The book is heavily focused
on MPLS, SDN, Segment-Routing, BGP, L2VPN/L3VPNs, over-all traffic engineering and much more. These are common terms within SP networks and the book does an incredible job in guiding the audience while exploring the device configurations in this topology.

![MPLS IN THE SDN ERA](mpls_in_the_sdn_era/images/mpls_sdn_era_topology.png)
This book goes through a number of device configurations in a multi-vendor lab topology
(Cisco IOSXR && Juniper)

*For this lab, all devices have been replaced with Cisco-IOSXR/XE as we are working on a
Cisco Certification.*

## Authors of the book:

- Antonio Sanchez Monge (Author)
- Krzysztof Grzegorz Szarkowicz (Author)

### To fully automate Service Provider Networks, you must understand Service Provider Networks.

[Get the book](https://www.amazon.com/MPLS-SDN-Era-Interoperable-Scenarios/dp/149190545X/ref=sr_1_1?dchild=1&keywords=mpls+in+the+sdn+era&qid=1618100065&s=books&sr=1-1)

# What does this repository include & cover?

My goal is to gather all of my self-training in this repostiroy and cover all the major
Cisco Certified DevNet Specialist (300-535 SPAUTO) topics. Starting with NSO because I have zero exposure to it professionally.

## Extras:

There will be some extra material in this repository that can be an aid for other areas
including but not limited to:

    - Batfish
    - Nornir
# How can I use this repo to study?

I recommend for you to have access to a virtual lab environment that can run this
topology. There are a total of 17 devices running in the lab scenario. 8 of them are IOSXR devices, 
which can consume up to 3GB each.

At this time, the lab configurations are not fully built. Once that is complete, I will be including 
a lab topology file with all the necessary information, etc. to import into a EVE-NG.

[Checkout the Wiki!](https://github.com/h4ndzdatm0ld/mpls_in_the_sdn_era/wiki)

30% of the SPAUTO exam is around Automation and Orchestration platforms, such as NSO. I can't stress enough the importance of taking the time to 
setup an NSO instance to explore and take advantage of the many examples in this repository.


# Why rely on this complicated lab topology?

I learn better when I am doing, not just reading and specially when breaking things. Having this complicated topology, building all the services in an
automated way will be key to our success in passing the certification. There will be tons of material in the end that will cover all the topics in the exam.

TODO: "breakout sections for each major topic"
