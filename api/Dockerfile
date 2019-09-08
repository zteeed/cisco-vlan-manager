FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt
COPY ./src/ /app/src
COPY ./main.py /app/main.py
