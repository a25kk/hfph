
GIT = git
NPM = npm

GRUNT = ./node_modules/.bin/grunt
BOWER = ./node_modules/.bin/bower

all: test-once compile docs

compile: compile-theme
	# ----------------------------------------------------------------------- #
	# cp dist/theme* 
	# ----------------------------------------------------------------------- #

compile-theme:
	mkdir -p dist
	NODE_PATH=./node_modules $(GRUNT) compile-theme

bootstrap: clean
	mkdir -p dist
	$(NPM) link --prefix=./node_modules
	NODE_PATH=./node_modules $(GRUNT) sed:bootstrap
	$(BOWER) install

jshint:
	NODE_PATH=./node_modules $(GRUNT) jshint

test:
	NODE_PATH=./node_modules $(GRUNT) test --force --pattern=$(pattern)

test-once:
	NODE_PATH=./node_modules $(GRUNT) test_once --force --pattern=$(pattern)

test-dev:
	NODE_PATH=./node_modules $(GRUNT) test_dev --force --pattern=$(pattern)

test-ci:
	NODE_PATH=./node_modules $(GRUNT) test_ci

clean:
	mkdir -p dist
	rm -rf dist
	rm -rf node_modules
	rm -rf bower_components

clean-all: clean
	if test -f $(BOWER); then $(BOWER) cache clean; fi

.PHONY: compile bootstrap jshint test test-ci docs clean