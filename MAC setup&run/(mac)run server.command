cd ~/desktop/annes_tuck_shop/main

export FLASK_APP=ATS
export FLASK_DEBUG=0
open http://localhost:8000

flask run --host=0.0.0.0 --port 8000 --with-threads
