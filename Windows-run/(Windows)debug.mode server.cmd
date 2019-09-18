cd..
cd main
set FLASK_APP=ATS
set FLASK_ENV=development
:main
flask run --host=0.0.0.0 --port=4999
goto main
