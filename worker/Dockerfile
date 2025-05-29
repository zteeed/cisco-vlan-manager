FROM python:3.11
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt
COPY ./src /app/src
COPY ./config.py /app/config.py
COPY ./main.py /app/main.py
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["main.py"]
