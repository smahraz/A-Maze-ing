
NAME = a_maze_ing.py
CONFIG_FILE = default_config.txt


run:
	@python3 $(NAME) $(CONFIG_FILE)


install:
	@uv sync
	@uv pip install mlx-*.whl



debug:
	python3 -m pdb $(NAME)


lint:
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	python3 -m flake8 . --exclude .venv


lint-strict:
	python3 -m mypy . --strict
	python3 -m flake8 . --exclude .venv


build:
	@uv build


clean:
	rm -vrf **/__pycache__/
	rm -vrf .mypy_cache


PHONY: install run debug lint-strict lint build
