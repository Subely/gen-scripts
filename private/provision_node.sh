#!/bin/sh

# install needed packages
pkg install -y ezjail

### Config Files ###

#pf
[ -f /etc/pf.conf ] && mv /etc/pf.conf /etc/pf.conf.bak
cat <<EOF > /etc/pf.conf
ext_if="vtnet0"
jail_if="lo1"
nat on \$ext_if from (\$jail_if) to any -> (\$ext_if)
EOF

# ezjail
[ -f /etc/pf.conf ] && mv /usr/local/etc/ezjail.conf /usr/local/etc/ezjail.conf.bak
cat <<EOF > /usr/local/etc/ezjail.conf
ezjail_use_zfs="YES"
ezjail_use_zfs_for_jails="YES"
ezjail_jailzfs="zroot/ezjail"
EOF

### Services ###

sysrc cloned_interfaces="lo1"
sysrc ifconfig_lo1="inet 127.1.0.0/16"
service netif cloneup

sysrc pf_enable=yes
service pf start

sysrc ezjail_enable=yes
service ezjail start

### Init ezjail ###
ezjail-admin install