FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt
COPY ./src/ /app/src
COPY ./static/ /app/static
COPY ./templates/ /app/templates
COPY ./config.py /app/config.py
COPY ./main.py /app/main.py
