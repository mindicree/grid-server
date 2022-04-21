#! /bin/bash

thelabel=$1
cat $thelabel >/dev/tcp/192.168.50.249/9100
