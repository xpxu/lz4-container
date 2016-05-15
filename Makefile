
PROJECT_DIR = `pwd`
UNIT_TEST_DIR = $(PROJECT_DIR)/tests
BUILD_DIR = $(PROJECT_DIR)/builddir
DATE = `date +"%m-%d-%y"`

init:
	pip install nose

test:
	@echo
	@echo 'running unit tests ...'
	@nosetests -v ${UNIT_TEST_DIR}

src:
	python setup.py sdist --dist-dir $(BUILD_DIR)

clean:
	find . -name '*.pyc' | xargs rm -rf
	rm -rf $(BUILD_DIR)
	rm -rf ./*.egg-info
	rm -rf setup.cfg
