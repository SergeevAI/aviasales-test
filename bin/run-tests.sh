#!/usr/bin/env bash
py.test ./ -v --pylint --pylint-j 0 --pylint-rcfile=./pylintrc --cov ./
pytest