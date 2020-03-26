#!/bin/bash
git clone https://github.com/sean-maclane/cpsc-449-group-c-project-1.git
cd cpsc-449-group-c-project-1
python3 -m venv venv
. venv/bin/activate
pip install -e .
pip install '.[test]'
