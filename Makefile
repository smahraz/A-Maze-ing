
NAME = a_maze_ing.py
CONFIG_FILE = default_config.txt


run:
	@python3 $(NAME) $(CONFIG_FILE)


install:
	pip install mlx-*.whl


debug:
	python3 -m pdb $(NAME)


lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	@python3 -m pip install --quiet --upgrade build
	@python3 -m build


clean:
	rm -vrf */__pycache__ */*/__pycache__
	rm -vrf .mypy_cache


.PHONY: install run debug lint build clean
