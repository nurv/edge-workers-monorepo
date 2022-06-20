import requests
import time
import board
import adafruit_dht
import psutil
import json
# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D4)
while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        data = [{"payload": json.dumps({'temp': temp, 'hum': 41})}]
        requests.post('http://localhost:5555/6549eb0f-5d61-4848-8239-6d1a3883e974', json=data)
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        print(error)
    time.sleep(10.0)
