
dev:
	pip install -e .[dev]

tests:
	pytest src

black:
	black -l 82 src --exclude "/(__pythran__|doc/_build|\.ipynb_checkpoints/*)/"
