pipcompile:
	pip-compile --upgrade --generate-hashes --output-file requirements/base.txt requirements/base.in
	pip-compile --upgrade --generate-hashes --output-file requirements/dev.txt requirements/dev.in
	pip-compile --upgrade --generate-hashes --output-file requirements/prod.txt requirements/prod.in

pipsync:
	pip-sync requirements/base.txt requirements/dev.txt

coverage:
	rm -rf htmlcov
	DJANGO_TEST=1 coverage run manage.py test
	coverage html
	firefox htmlcov/index.html