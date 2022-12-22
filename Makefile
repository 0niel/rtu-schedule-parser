.PHONY: format
format:
	isort --recursive --force-single-line-imports --apply rtu_schedule_parser
	isort --recursive --force-single-line-imports --apply tests
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place rtu_schedule_parser --exclude=__init__.py
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place tests --exclude=__init__.py
	black rtu_schedule_parser
	black tests
	isort --recursive --apply rtu_schedule_parser
	isort --recursive --apply tests

.DEFAULT_GOAL :=