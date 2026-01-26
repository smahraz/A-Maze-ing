
NAME = a_maze_ing.py
CONFIG_FILE = default_config.txt



run:
	@python3 $(NAME) $(CONFIG_FILE)


install:
	@uv pip install -r pyproject.toml
	@uv pip install mlx-*.whl



debug:
	python3 -m pdb $(NAME)


lint:
	flake8 . --exclude venv
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	python3 -m mypy . --strict



clean:
	rm -vrf **/__pycache__/
	rm -vrf .mypy_cache


PHONY: install run debug lint-strict lint
