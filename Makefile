check:
	flake8 flake8_super_mario
	mypy flake8_super_mario
	make test

test:
	python -m pytest --cov=flake8_super_mario --cov-report=xml -p no:warnings --disable-socket
