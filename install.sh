#!/usr/bin/env bash

set -ex

ssh "client1.$red_exp_name.offtech" "~/$folder_name/red/install.sh" &
ssh "client2.$red_exp_name.offtech" "~/$folder_name/red/install.sh" &
ssh "client3.$red_exp_name.offtech" "~/$folder_name/red/install.sh" &
ssh "server.$blue_exp_name.offtech" "sudo apt-get install -y iftop" &
ssh "gateway.$blue_exp_name.offtech" "sudo apt-get install -y iftop" &

wait
