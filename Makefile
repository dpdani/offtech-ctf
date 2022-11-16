.PHONY: install upload prepare-dependencies upload-dependencies


user_name=`cat deter_username.txt`
folder_name="ctf-resilient"
exp_name="flagctf2"


install:
	ssh $(user_name)@users.isi.deterlab.net<<'EOF'
		ssh client1.$(exp_name).offtech "sudo apt-get install -y tcpreplay iftop"
		ssh client2.$(exp_name).offtech "sudo apt-get install -y tcpreplay iftop"
		ssh client3.$(exp_name).offtech "sudo apt-get install -y tcpreplay iftop"
	EOF


upload:
	rsync -avz --exclude-from='.rsyncignore' . $(user_name)@users.isi.deterlab.net:~/$(folder_name)

prepare-dependencies:
	rm -rf site-packages
	ssh $(user_name)@users.isi.deterlab.net "rm -rf ~/ctf-resilient/site-packages"
	cp -r ~/.pyenv/versions/ctf-red/lib/python3.6/site-packages/ .

upload-dependencies: prepare-dependencies upload
