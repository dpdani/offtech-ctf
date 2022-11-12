.PHONY: install upload prepare-dependencies upload-dependencies


user_name=`cat deter_username.txt`
folder_name="ctf-resilient"


install:
	sudo apt install python3-pip tcpreplay
	sudo pip install --update pip
	curl https://pyenv.run | bash
	pyenv install 3.11
	pyenv shell 3.11 <<EOF
		pip install -U pip
		pip install -e .
	EOF


upload:
	rsync -avz --exclude-from='.rsyncignore' . $(user_name)@users.isi.deterlab.net:~/$(folder_name)

prepare-dependencies:
	rm -rf site-packages
	ssh otech2ac@users.isi.deterlab.net "rm -rf ~/ctf-resilient/site-packages"
	cp -r ~/.pyenv/versions/ctf-red/lib/python3.6/site-packages/ .

upload-dependencies: prepare-dependencies upload
