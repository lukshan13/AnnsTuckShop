cd..
cd main
set FLASK_APP=ATS
set FLASK_DEBUG=0
:main
flask run --host=0.0.0.0 --port 8001 --with-threads

goto main
pause