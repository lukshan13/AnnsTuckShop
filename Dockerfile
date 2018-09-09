FROM python:3.6

COPY Installers/linux.sh /tmp/.ats_install.sh 
RUN sh /tmp/.ats_install.sh && rm /tmp/.ats_install.sh

COPY Main /opt/ATS_Main

WORKDIR /opt/ATS_main

ENTRYPOINT \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8 \ 
	FLASK_APP=ATS \
	FLASK_ENV=production \
	flask run --host=0.0.0.0 --with-threads
