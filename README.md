# Amper monitor
This project is for monitor electric energy in house.

## Install

```bash
cp .env-example .env
# set SERIAL_PORT in .env

# move to /amper-exporter
docker build -t amper-exporter . 
```

## Usage

```bash
docker-compose up
```
