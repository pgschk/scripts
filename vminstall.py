#!/usr/bin/python
#
# Q'n'D vm setup script (works only for my KVM box)
#
# Copyright (c) 2011 Philipp Geschke
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
####################################

import os,sys
name = str(raw_input("Please enter the systems name: "))
size = int(raw_input("Please enter the systems disk size in Gigabytes: "))
mem = int(raw_input("Please enter the systems memory in Megabytes: "))
ostype = raw_input("Please enter the type of operating system you want to install (Ubuntu 12.04 [u], Debian 6.0[d], CentOS 5.4[c], FreeBSD 8.1[f], Ubuntu 12.04 Desktop [ud]): ")
net = raw_input("Please enter the virtnet to connect to [virtnet0]")
family = "linux"

if net == "":
    net = "virtnet0"

if ostype == "u":
    variant = "ubuntukarmic"
    iso = "ubuntu-12.04-server-amd64.iso"
elif ostype == "ud":
    variant = "ubuntukarmic"
    iso = "ubuntu-12.04-desktop-amd64.iso"
elif ostype == "d":
    variant = "debiansqueeze"
    iso = "debian-6.0.1a-amd64-netinst.iso"
elif ostype == "c":
    variant = "rhel5.4"
    iso = "CentOS-5.4-x86_64-bin-DVD.iso"
elif ostype == "f":
    family = "unix"
    variant = "freebsd7"
    iso = "FreeBSD-8.1-RELEASE-amd64-disc1.iso"
else:
    print("Unknown Operating System. Exit.")
    exit


command_lvm = "/sbin/lvcreate -L" + str(size) + "G -n " + name + "_disk vg0"
command_virt = "/usr/bin/virt-install --connect qemu:///system -n " + name + " -r " + str(mem) + " --vcpus=2 --disk path=/dev/vg0/" + name + "_disk --vnc --serial pty --noautoconsole --os-type " + family  + " --os-variant " + variant + " --accelerate --network=network:" + net + " --hvm -k de -c /isos/" + iso

sys.stdout.write("Creating logical volume for domain " + name + "...")
os.system(command_lvm)
print("done")
print("Creating virtual machine " + name)
os.system(command_virt)
