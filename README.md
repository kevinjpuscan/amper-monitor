# Amper monitor
This project is for monitor electric energy in house.

## Install

```bash
# move to /amper-exporter
cp .env-example .env
# set SERIAL_PORT
docker build -t amper-exporter . 
```

## Usage

```bash
docker-compose up
```
