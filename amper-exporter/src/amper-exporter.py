import datetime
import os
from prometheus_client import make_wsgi_app, Gauge
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
amper = Gauge('amper_energy_kwh','Energy consumed in kwh',['month','day'])

def get_amper_value():
  ARDUINO.write('b'.encode())
  valueInput = ARDUINO.readline().decode()
  print('corriente:'+valueInput)
  return valueInput

@app.route("/metrics")
def updateResults():
    current_dt = datetime.datetime.now()
    r_amper=get_amper_value()
    day_label=current_dt.strftime("%Y-%m-%d")
    month_label=current_dt.strftime("%Y-%m")
    amper.labels(month_label,day_label).set(r_amper)
    print(current_dt.strftime("%d/%m/%Y %H:%M:%S - ") + "Amper: "+ str(r_amper))
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

