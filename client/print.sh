#! /bin/bash

thelabel=$1
cat $thelabel >/dev/tcp/192.168.50.251/9100
