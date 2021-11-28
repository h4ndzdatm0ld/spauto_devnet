# Installing NSO Evaluation Version (5.5)
For my studies, I decided to deploy an Ubuntu VM to host an NSO instance. Keep in mind there are several ways to take advantage of NSO. Within a CI/CD pipeline, as a docker container, a full blown production server and as a local install. An evaluation version has recently been released and is free to download.

Head on over to the following site and get the installer files.

[NSO Eval](https://developer.cisco.com/docs/nso/#!getting-and-installing-nso/download-your-nso-free-trial-installer-and-cisco-neds)

Although the EVAL version comes with a variety of NEDs included, go ahead and download the latest available NEDS as well. You will need a DevNet account to log in and download.

Later on, we will cover how to set up NSO in a docker container which is useful for CI/CD.

[NSO Docker](https://github.com/NSO-developer/nso-docker)

At this point, you should have downloaded a local copy of the eval version on your machine. I will assume that you have a fresh install of Ubuntu 20.04 server running. 

Our VM will have 2 CPU's and 4GB of ram. This should be plenty for our operations, although more RAM may be required if we add all 17 routers, as documentation suggests. We will be doing a Local Install on our remote server which allows the creation of multiple, unrelated NSO instances in one host.

## Getting started
I won't bore you with the details, but the first step is to SCP the .bin file for the NSO appliance and any other NEDs you may have downloaded to our VM.

Start with a system package update and then lets make sure we have the following installed:

```
sudo apt-get install default-jdk &&\
python3-pip &&\
```
Now install paramiko via pip
```	
pip3 install paramiko 
```

It's recommended to install our NSO instance in our HOME directory. But we must first unpack all the contents of our NSO .bin file.

Change directory to where you SCP'd the files onto the remote server and perform the following:

```
sh nso-5.5.linux.x86_64.signed.bin --skip-verification
```

Now that the files are unpacked, lets go ahead and install a local instance in our home directory. We are able to install several different instances this way. Only one of our instances can be running at any given time, but if you would like to have more than one, just simply create more with different names. 

```
sh nso-5.5.linux.x86_64.installer.bin $HOME/ncs-5.5 --local-install
```

Finally, set up our env
```
source $HOME/ncs-5.5/ncsrc
ncs-setup --dest $HOME/ncs-run
```
Now back out to the root dir where we installed our local instance and run the NCS server from the ncs-run directory.

```
cd ..
cd ncs-run
ncs
```

## Example:
```
htinoco@nso-dev-example:~$ cd NSO-Files/

htinoco@nso-dev-example:~/NSO-Files$ sh nso-5.5.linux.x86_64.installer.bin $HOME/ncs-5.5 --local-install
INFO  Using temporary directory /tmp/ncs_installer.12458 to stage NCS installation bundle
INFO  Unpacked ncs-5.5 in /home/htinoco/ncs-5.5
INFO  Found and unpacked corresponding DOCUMENTATION_PACKAGE
INFO  Found and unpacked corresponding EXAMPLE_PACKAGE
INFO  Found and unpacked corresponding JAVA_PACKAGE
INFO  Generating default SSH hostkey (this may take some time)
INFO  SSH hostkey generated
INFO  Environment set-up generated in /home/htinoco/ncs-5.5/ncsrc
INFO  NSO installation script finished
INFO  Found and unpacked corresponding NETSIM_PACKAGE
INFO  NCS installation complete
htinoco@nso-dev-example:~/NSO-Files$ 
htinoco@nso-dev-example:~/NSO-Files$ source $HOME/ncs-5.5/ncsrc
htinoco@nso-dev-example:~/NSO-Files$ ncs-setup --dest $HOME/ncs-run
htinoco@nso-dev-example:~/NSO-Files$ 
htinoco@nso-dev-example:~/NSO-Files$ cd ..
htinoco@nso-dev-example:~$ cd ncs-run/
htinoco@nso-dev-example:~/ncs-run$ ncs
htinoco@nso-dev-example:~/ncs-run$ 
```
# Installing Additional NEDS

Although NSO instance comes pre-packaged with several NEDs available, there are a couple different free eval versions available for download through the DevNet website as well.

[NSO Files / Neds](https://developer.cisco.com/docs/nso/#!getting-and-installing-nso/download-your-nso-free-trial-installer-and-cisco-neds)

NEDS are Network Element Drivers, which NSO uses to communicate with different vendor devices.

Lets go through installing our additional NEDS we've downloaded for Cisco IOSXR & XE.

--- 
```
htinoco@nso-dev-example:~/NSO-Files/neds$ tree
.
├── ncs-5.5-cisco-ios-6.69.1.signed.bin
└── ncs-5.5-cisco-iosxr-7.33.1.signed.bin

0 directories, 2 files
```

Notice these files are also signed .bin

## Unpack the files (Skip verification)
Just like our NSO installer file, we have to unpack the contents of the files. 

```
htinoco@nso-dev-example:~/NSO-Files/neds$ sh ncs-5.5-cisco-iosxr-7.33.1.signed.bin --skip-verification
Unpacking...
htinoco@nso-dev-example:~/NSO-Files/neds$ sh ncs-5.5-cisco-ios-6.69.1.signed.bin --skip-verification
Unpacking...
htinoco@nso-dev-example:~/NSO-Files/neds$ tree
.
├── cisco_x509_verify_release.py
├── cisco_x509_verify_release.py3
├── ncs-5.5-cisco-ios-6.69.1.signed.bin
├── ncs-5.5-cisco-ios-6.69.1.tar.gz
├── ncs-5.5-cisco-ios-6.69.1.tar.gz.signature
├── ncs-5.5-cisco-iosxr-7.33.1.signed.bin
├── ncs-5.5-cisco-iosxr-7.33.1.tar.gz
├── ncs-5.5-cisco-iosxr-7.33.1.tar.gz.signature
├── README.signature
└── tailf.cer

0 directories, 10 files
htinoco@nso-dev-example:~/NSO-Files/neds$ 
```

Now that we have the tarball files of each NED, lets extract the contents in to the correct folder within our new NSO installation directory.

Lets just back to the directory of our NSO install:
```
cd ~/ncs-5.5
```
Move into the NEDS folder:
```
cd packages/neds
```
Extract the tarballs in this directory from the remote directory:
```
tar -zxvf ~/NSO-Files/neds/ncs-5.5-cisco-iosxr-7.33.1.tar.gz 
tar -zxvf ~/NSO-Files/neds/ncs-5.5-cisco-ios-6.69.1.tar.gz 
```

We should now have a total of 12 directories, with the two new additional NEDs.
```
htinoco@nso-dev-example:~/ncs-5.5/packages/neds$ tree -L 1
.
├── a10-acos-cli-3.0
├── alu-sr-cli-3.4
├── cisco-asa-cli-6.6
├── cisco-ios-cli-3.0
├── cisco-ios-cli-3.8
├── cisco-ios-cli-6.69
├── cisco-iosxr-cli-3.0
├── cisco-iosxr-cli-3.5
├── cisco-iosxr-cli-7.33
├── cisco-nx-cli-3.0
├── dell-ftos-cli-3.0
└── juniper-junos-nc-3.0

12 directories, 0 files
```

We have successfully installed our NEDs.

# Creating Local Instance of NSO

Our local installation allows us to have several NSO instances. We will create an example
instance.

Use the 'ncs-setup' command to create a new NSO instance.
--package is used to specify the NEDS
--dest flag is used to specifcy a directory for the new nso-instance.
```
ncs-setup --package ~/ncs-5.5/packages/neds/cisco-ios-cli-6.69/ \
--package ~/ncs-5.5/packages/neds/cisco-iosxr-cli-7.33/ \
--dest example-nso-instance
```
## Starting NSO Instance

It's important to navigate to the folder of the new NSO instance.
From our example above, we created a new directory called 'example-nso-instance'

cd into this directory and run the following command:

```bash
ncs
```

That's it!

## Access the NSO Instance

If you don't remember the IP of the server, simply do the following:

```bash
ip addr | grep inet
```

Example:

```bash
htinoco@nso-dev-example:~/ncs-run$ ip addr | grep inet
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
    inet 192.168.0.54/23 brd 192.168.1.255 scope global dynamic ens160
```

The local install should be reachable at http://x.x.x.x:8080/login.html.

So, based on our example.. open a web browser and go to the following address:

http://192.168.0.54:8080/login.html

## Credentials

Default credentials are admin/admin.
