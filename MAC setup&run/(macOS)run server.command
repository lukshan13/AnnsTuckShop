cd ~/desktop/anns_tuck_shop/main

export FLASK_APP=ATS
export FLASK_ENV=production
bash -c 'while [ 0 ]; do flask run --host=0.0.0.0 --port 8000 --with-threads;done'