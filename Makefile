.PHONY: install


install:
	curl https://pyenv.run | bash
	pyenv install 3.11
	pyenv shell 3.11 <<EOF
		pip install -U pip
		pip install -e .
	EOF
