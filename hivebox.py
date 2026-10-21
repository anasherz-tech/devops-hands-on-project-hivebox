"""Endpoint: /version and Endpoint: /temperature"""
import datetime as dt
import requests
from flask import Flask
from project import VERSION

app = Flask(__name__)
SENSEBOX_IDS = ["5eba5fbad46fb8001b799786", "5c21ff8f919bf8001adf2488", "5ade1acf223bd80019a1011c"]

@app.route("/version")
def print_version():
    """Return the version of the app"""

    return {"version":VERSION}

@app.route("/temperature")
def avg_temp():
    """ Return current average temperature based on all senseBox data and Ensure that 
    the data is no older than 1 hour. """

    fresh_sensors = []
    for sensebox_id in SENSEBOX_IDS:
        r = requests.get("https://api.opensensemap.org/boxes/" + sensebox_id, timeout=20)
        data = r.json()
        for sensor in data['sensors']:
            if sensor.get('title') == 'Temperatur':
                print(float(sensor['lastMeasurement']['value']))
                print(sensor['lastMeasurement']['createdAt'])
                time_now = dt.datetime.now(tz=dt.UTC)
                current_sensor_reading = sensor['lastMeasurement']['createdAt']
                reading = time_now - (dt.datetime.fromisoformat(current_sensor_reading))
                print(reading)
                if reading < dt.timedelta(hours=1):
                    print("Fresh")
                    fresh_sensors.append(float(sensor['lastMeasurement']['value']))
                else:
                    print("Old")
    print(fresh_sensors)


    if fresh_sensors:
        sum_fresh_sensors = sum(fresh_sensors)
        len_fresh_sensors = len(fresh_sensors)
        avg_fresh_sensors = sum_fresh_sensors / len_fresh_sensors
        print(avg_fresh_sensors)
        return {"temperature":avg_fresh_sensors}
    print("All sensors are giving old value")
    return {"temperature":"All sensors are giving old value"}
