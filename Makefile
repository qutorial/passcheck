test:
	bash -c ". activate.sh; ./run.tests.sh; deactivate"

install:
	bash -c ". install.sh"

uninstall: clean
	bash -c ". uninstall.sh"

clean:
	find . -name "__pycache__" -exec rm -rf {} \; 2>/dev/null
	find . -name "*.pyc" -exec rm -f {} \; 2>/dev/null
