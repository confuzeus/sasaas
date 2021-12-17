#!/bin/bash

set -e

pip-compile --upgrade --generate-hashes --output-file requirements/base.txt requirements/base.in
pip-compile --upgrade --generate-hashes --output-file requirements/dev.txt requirements/dev.in
pip-compile --upgrade --generate-hashes --output-file requirements/prod.txt requirements/prod.in