FROM arm32v7/python:3.6-buster

WORKDIR /app

COPY src/requirements.txt requirements.txt

RUN pip install -r requirements.txt && \
    rm requirements.txt

COPY src/. .

EXPOSE 9798

CMD ["python", "amper-exporter.py"]
