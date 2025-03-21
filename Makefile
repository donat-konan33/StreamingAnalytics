include /home/dk.busimanager/code/donat-konan33/data-engineering-challenges/make.inc

test: pytest-and-write-output

run:
	poetry run python lwqueue/ui.py
