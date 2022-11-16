.PHONY: install upload prepare-dependencies upload-dependencies


user_name=`cat deter_username.txt`
folder_name="ctf-resilient"
red_exp_name="ctf-resilient-g3"
blue_exp_name="ctf-resilient-g3"


install:
	red_exp_name=$(red_exp_name) blue_exp_name=$(blue_exp_name) folder_name=$(folder_name) ./install.sh

upload:
	rsync -avz --exclude-from='.rsyncignore' . $(user_name)@users.isi.deterlab.net:~/$(folder_name)

prepare-dependencies:
	rm -rf site-packages
	ssh $(user_name)@users.isi.deterlab.net "rm -rf ~/ctf-resilient/site-packages"
	cp -r ~/.pyenv/versions/ctf-red/lib/python3.6/site-packages/ .

upload-dependencies: prepare-dependencies upload

analyzer:
	cd blue && ssh -T $(user_name)@users.isi.deterlab.net ssh -T $(machine).ctf-resilient-g3.offtech "sudo tcpdump -s0 -U --immediate-mode -nn -i $(interface) -w -" | python3 analyze_pcap.py

drop-resets:
	# This is for the malicious client to silence the kernel's RSTs
	sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
