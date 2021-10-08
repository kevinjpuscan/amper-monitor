FROM python:3.9.6-alpine3.13

WORKDIR /app

COPY src/. .

RUN pip install -r requirements.txt && \
    rm requirements.txt

EXPOSE 9798

CMD ["python", "amper-exporter.py"]