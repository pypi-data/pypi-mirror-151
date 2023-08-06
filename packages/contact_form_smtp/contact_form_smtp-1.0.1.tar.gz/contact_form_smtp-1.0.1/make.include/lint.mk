# lint / source format

lint_src = $(module) tests docs

# blacken python source (code formatter)
fmt: lint

# check style, lint with flake8
lint:
	isort $(lint_src)
	black $(lint_src)
	flake8 --config tox.ini $(lint_src)

# vim:ft=make
