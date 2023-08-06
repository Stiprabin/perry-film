COPY requirements.txt
RUN apt-get update
RUN --rm -it -v $PWD/data:/data ultrafunk/undetected-chromedriver
RUN pip install -r requirements.txt
CMD gunicorn app:app --workers 4 --threads 2
