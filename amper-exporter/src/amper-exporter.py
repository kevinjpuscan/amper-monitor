from datetime import datetime, timedelta
import os
from prometheus_client import make_wsgi_app, Gauge, Counter
from flask import Flask
from waitress import serve
import serial,time
from dotenv import load_dotenv
import atexit

load_dotenv()

SERIAL_PORT=os.getenv('SERIAL_PORT')
PORT=9798
ARDUINO={}

app = Flask("Amper-Exporter")  # Create flask app
energy_w = Gauge('amper_energy_w','Energy consumed in w')
energy_day_w = Gauge('amper_energy_day_w','Energy consumed in w with label day',['day'])
energy_month_w = Gauge('amper_energy_month_w','Energy consumed in w with label month',['month'])
power_month =Counter('amper_power_month','Total Kwh consumed by month with label month',['month'])
power_day =Counter('amper_power_day','Total Kwh consumed by month with label day',['day'])

last_day = "2021-01-01"
last_month = "2021-01"

def get_amper_value():
  ARDUINO.write('b'.encode())
  valueInput = ARDUINO.readline().decode()
  print('corriente:'+valueInput)
  return valueInput

@app.route("/metrics")
def updateResults():
	global last_day
	global last_month

	current_dt = datetime.now()
	location_dt=current_dt-timedelta(hours=5)
	amper_w=float(get_amper_value())
	amper_kw=amper_w/1000
	day_label=location_dt.strftime("%Y-%m-%d")
	month_label=location_dt.strftime("%Y-%m")

	energy_w.set(amper_w)
	energy_month_w.labels(month_label).set(amper_w)
	energy_day_w.labels(day_label).set(amper_w)

	if day_label!=last_day:
		last_day=day_label
		power_day.clear()
	
	if month_label!=last_month:
		last_month=month_label
		power_month.clear()

	power_month.labels(month_label).inc(amper_kw/6)
	power_day.labels(day_label).inc(amper_kw/6)
	print(current_dt.strftime("%d/%m/%Y %H:%M:%S - ") + "Amper: "+ str(amper_kw))
	return make_wsgi_app()


@app.route("/")
def mainPage():
    return ("<h1>Welcome to Amper-Exporter.</h1>" +
            "Click <a href='/metrics'>here</a> to see metrics.")

@atexit.register 
def exit(): 
    ARDUINO.close()
    print("Exiting to Amper-Exporter!")

if __name__ == '__main__':
    ARDUINO=serial.Serial(SERIAL_PORT, 9600, timeout=1)
    time.sleep(3)
    print("Starting Amper-Exporter on http://localhost:" + str(PORT) + " | SerialPort:" +str(SERIAL_PORT))
    serve(app, host='0.0.0.0', port=PORT)

