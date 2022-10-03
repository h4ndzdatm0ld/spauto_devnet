# Cisco DevNet SP Automation Playground & Study Notes!

All of the study notes have now been moved to use auto-generated documentation to build a static site with Github Pages. Alongside all the code documentation, you will find a folder structure for notes in markdown broken down by test categories.

[Documentation + Study Notes](https://h4ndzdatm0ld.github.io/spauto_devnet/index.html)

Build local

```bash
sphinx-build -vvv -b html ./docs ./docs/public
cd docs/public
python -m http.server
```

## A lab topology based on MPLS in the SDN era book used for 300-535 SPAUTO studies

[Cisco Certified DevNet Specialist - Service Provider Automation and Programmability](https://developer.cisco.com/certification/devnet-sp-auto/)

### Why MPLS in the SDN Era?

Simple. This is an incredible book for any and all Network Engineers interested in learning technologies used in Service Provider environments. The book is heavily focused on MPLS, SDN, Segment-Routing, BGP, L2VPN/L3VPNs, over-all traffic engineering and much more. These are common terms within SP networks and the book does an incredible job in guiding the readers while exploring the device configurations in this topology. However, many other topics are not covered by the book and this repository will hopefully fill in the gaps. This book lays the foundation for our lab topology, but it has increased and grown over time. Additional material used for studying is the book `Network Programmability with YANG`, which covers a lot of the topics in the blueprint!

![MPLS IN THE SDN ERA](./docs/images/mpls_sdn_era_topology.png)

This book goes through a number of device configurations in a multi-vendor lab topology (Cisco IOSXR && Juniper). However, _For this lab, all devices have been replaced with Cisco-IOSXR/XE as we are working on a Cisco Certification._

### To fully automate Service Provider Networks, you must understand Service Provider Networks

[MPLS in the SDN Era](https://www.amazon.com/MPLS-SDN-Era-Interoperable-Scenarios/dp/149190545X/ref=sr_1_1?dchild=1&keywords=mpls+in+the+sdn+era&qid=1618100065&s=books&sr=1-1)

[Network Programmability with YANG](https://www.amazon.com/Network-Programmability-YANG-Modeling-driven-Management/dp/0135180392)

## What does this repository include & cover

My goal is to gather all of my self-training in this repository and cover all the topics of the Cisco Certified DevNet Specialist (300-535 SPAUTO) certification.

## How can I use this repo to study?

I recommend you read the documentation and additionally, take advantage of the ContainerLab topology provided. Use and abuse the topology. Destroy and rebuild. Learn by breaking!

Go ahead and start the topology using ContainerLab and have fun automating the network!

30% of the SPAUTO exam is around Automation and Orchestration platforms, such as NSO. I can't stress enough the importance of taking the time to setup an NSO instance to explore and take advantage of the many examples in this repository. Containerizing NSO for CI/CD is also part of the blueprint, which we will cover.

## Recommended Study Material & Resources

    - MPLS in the SDN Era (Book)
    - Network Programmability with YANG (Book)
    - Nicholas Russo DevNet Material (Pluralsight)

## Container Lab

After exploring [ContainerLab](https://containerlab.srlinux.dev/), I have begun to move away from EVE-NG and completely dockerized this topology. Initially, I thought I would share an exported lab from EVE-NG, but including the CLAB topology in this lab makes it so much more portable.

I've created a simple to use docker-compose service to start the lab. ContainerLab it's self is pulled down as a docker container, so you don't need a local installation of ContainerLab unless you want to have one. I recommend you deploy this lab in a Linux environment, as docker virtualization will prevent you from starting in a Mac or Windows env.

### Requirements

- Docker
- Docker Compose
- Roughly 32Gb of available RAM

### Starting Lab

Simply run the service using docker-compose

```bash
docker-compose run clab
```

You should see something similar to this

```text
➜  spauto_devnet git:(containerlab) ✗ docker-compose run clab
Creating spauto_devnet_clab_run ... done
INFO[0000] Parsing & checking topology file: spauto-topology.yml
INFO[0000] Creating lab directory: /src/clab-spauto-topology.yml
INFO[0000] Creating docker network: Name='spauto', IPv4Subnet='172.100.100.0/24', IPv6Subnet='2001:172:100:100::/80', MTU='1500'
INFO[0000] Creating container: xrv-pe1
INFO[0000] Creating container: xrv-rr-1
INFO[0000] Creating container: xrv-p2
INFO[0000] Creating container: xrv-p1
INFO[0000] Creating container: xrv-rr-2
INFO[0000] Creating container: xrv-pe2
INFO[0000] Creating container: xrv-pe3
INFO[0000] Creating container: xrv-pe4
INFO[0001] Creating virtual wire: xrv-pe1:eth4 <--> xrv-pe2:eth3
INFO[0002] Creating virtual wire: xrv-pe2:eth4 <--> xrv-p2:eth1
INFO[0002] Creating virtual wire: xrv-pe4:eth1 <--> xrv-p2:eth6
INFO[0002] Creating virtual wire: xrv-pe1:eth5 <--> xrv-p1:eth2
INFO[0002] Creating virtual wire: xrv-p1:eth5 <--> xrv-p2:eth4
INFO[0002] Creating virtual wire: xrv-p1:eth4 <--> xrv-p2:eth3
INFO[0002] Creating virtual wire: xrv-rr-2:eth1 <--> xrv-p1:eth6
INFO[0002] Creating virtual wire: xrv-rr-2:eth3 <--> xrv-p2:eth5
INFO[0003] Creating virtual wire: xrv-pe3:eth3 <--> xrv-pe4:eth2
INFO[0003] Creating virtual wire: xrv-pe3:eth2 <--> xrv-p1:eth7
INFO[0003] Creating virtual wire: xrv-rr-1:eth4 <--> xrv-p2:eth2
INFO[0003] Creating virtual wire: xrv-rr-1:eth2 <--> xrv-p1:eth3
INFO[0003] Creating virtual wire: xrv-rr-1:eth3 <--> xrv-rr-2:eth2
INFO[0004] Adding containerlab host entries to /etc/hosts file
Run 'containerlab version upgrade' to upgrade or go check other installation options at https://containerlab.srlinux.dev/install/
+---+-----------------------------------+--------------+---------------------------+--------+---------+--------------------+--------------------------+
| # |               Name                | Container ID |           Image           |  Kind  |  State  |    IPv4 Address    |       IPv6 Address       |
+---+-----------------------------------+--------------+---------------------------+--------+---------+--------------------+--------------------------+
| 1 | clab-spauto-topology.yml-xrv-p1   | eef17ad66ff1 | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.101/24 | 2001:172:100:100::101/80 |
| 2 | clab-spauto-topology.yml-xrv-p2   | 24e5fc6af015 | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.102/24 | 2001:172:100:100::102/80 |
| 3 | clab-spauto-topology.yml-xrv-pe1  | efb11d90a5eb | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.11/24  | 2001:172:100:100::11/80  |
| 4 | clab-spauto-topology.yml-xrv-pe2  | 7d604f4f06f8 | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.22/24  | 2001:172:100:100::22/80  |
| 5 | clab-spauto-topology.yml-xrv-pe3  | 285733f28608 | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.33/24  | 2001:172:100:100::33/80  |
| 6 | clab-spauto-topology.yml-xrv-pe4  | 5af4945fab68 | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.44/24  | 2001:172:100:100::44/80  |
| 7 | clab-spauto-topology.yml-xrv-rr-1 | b5084e97738d | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.201/24 | 2001:172:100:100::201/80 |
| 8 | clab-spauto-topology.yml-xrv-rr-2 | 6a80d3285c2e | h4ndzdatm0ld/vr-xrv:6.1.3 | vr-xrv | running | 172.100.100.202/24 | 2001:172:100:100::202/80 |
+---+-----------------------------------+--------------+---------------------------+--------+---------+--------------------+--------------------------+
```

This will start a lab topology for you and all the devices should be accessible via SSH/NETCONF/gNMI. The topology YAML file has been crafted with a custom Docker Management Network to statically assign the IP's to each node as well. This network is reserved under 172.100.100.0/24. From your local machine, after starting the devices, you should be able to ssh into each one.

You will know the lab has been successfully started once all devices show healthy state. Validate via docker command

```
docker ps
```

The status should say (healthy)

### Load Configurations

Unfortunately, these vrnetlab based nodes don't support providing a startup-config via ContainerLab. However, I've provided a Nornir job to simply deploy all the configs to each one of the devices.

After starting the lab and waiting around 7 Minutes, launch off the Nornir script to deploy the configurations.

Install the project venv

```bash
poetry install
```

Activate venv

```bash
poetry shell
```

Locate the Nornir playground

```bash
cd spauto/spauto_nornir
```

Deploy configs with Nornir

```bash
python nr_deploy_configs.py
```

> > > NOTE: If you have issues with `no matching key exchange method found, add the below line to `~/.ssh/config`

```bash
Ciphers aes256-cbc,aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc
KexAlgorithms +diffie-hellman-group1-sha1
```

### Destroying the lab

To destroy the lab, simply override the docker-compose service command and destroy it.

```bash
docker-compose run clab containerlab destroy -t spauto-topology.yml
```

Example stats of running all 8 core XR Routers simultaneously.

```bash
CONTAINER ID   NAME                                CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O     PIDS
9d6acb79bcbe   clab-spauto-topology.yml-xrv-pe4    2.56%     1.769GiB / 62.71GiB   2.82%     259kB / 207kB    0B / 82.8MB   13
de723690af86   clab-spauto-topology.yml-xrv-p1     2.42%     1.719GiB / 62.71GiB   2.74%     204kB / 212kB    0B / 60.2MB   13
f0e0710d1edb   clab-spauto-topology.yml-xrv-pe1    2.41%     1.793GiB / 62.71GiB   2.86%     213kB / 168kB    0B / 59.2MB   13
aca6fb91120c   clab-spauto-topology.yml-xrv-pe3    1.89%     1.758GiB / 62.71GiB   2.80%     121kB / 56.9kB   0B / 52MB     13
63277aac88ef   clab-spauto-topology.yml-xrv-p2     1.47%     1.718GiB / 62.71GiB   2.74%     198kB / 204kB    0B / 59.1MB   13
c83b2faa5ea8   clab-spauto-topology.yml-xrv-pe2    2.02%     1.796GiB / 62.71GiB   2.86%     206kB / 146kB    0B / 57.7MB   13
35fcceedc92a   clab-spauto-topology.yml-xrv-rr-2   4.33%     1.744GiB / 62.71GiB   2.78%     185kB / 186kB    0B / 60.5MB   13
3f62259d2ae9   clab-spauto-topology.yml-xrv-rr-1   1.45%     1.745GiB / 62.71GiB   2.78%     190kB / 190kB    0B / 59.5MB   13
```

## NSO

A pre-packaged NSO Docker container is available. This will be a fresh docker container with the following NEDs:

```text
cisco-ios-cli-6.69
cisco-iosxr-cli-7.33
```

To spin up the NSO instance

```bash
docker-compose up -d nso
```

To access via UI (admin/admin) get the IP address of the NSO instance and open it in your browser

```bash
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

If you want to simply ssh from the same machine that's hosting the container

```bash
ssh admin@localhost -p 2024
```

The docker-compose service is mapping port 2024 to 22.
