#!/bin/bash
cd "$(dirname "$0")"/../main
export FLASK_APP=ATS
export FLASK_ENV=development
bash -c 'while [ 0 ]; do flask run --host=0.0.0.0 --port 5000 --with-threads;done'