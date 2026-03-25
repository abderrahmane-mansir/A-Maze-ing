run:
	@python3 a_maze_ing.py config.txt
install:
	@pip install blessed pygame flake8 mypy
package:
	@python3 -m pip install --upgrade pip build
	@python3 -m build
debug:
	@python3 -m pdb a_maze_ing
clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf build dist *.egg-info
lint:
	@flake8 .
	@mypy . \
  	  --warn-return-any \
      --warn-unused-ignores \
      --ignore-missing-imports \
      --disallow-untyped-defs \
      --check-untyped-defs
lint-strict:
	@flake8 .
	@mypy . --strict