import logging
import os
import forecastio
import requests
import json
from pyemojify import emojify

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

api_key = "8ac8a9f185a7384bdeae01ec9fadee8f"

#get weather

def get_weather():
    url = "http://ip-api.com/json/"
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr


    # ip = "2601:602:9804:4396:8d29:6f17:a182:e8ed"

    list = []

    r = requests.get(url+ip)
    json_string = json.dumps(r.json())
    json_obj = json.loads(json_string)
    if json_obj['status'] == "fail" :
        return [url+ip, emojify("Something went wrong :bee: :sunny: :umbrella:")]

    forecast = forecastio.load_forecast(api_key, json_obj['lat'], json_obj['lon'])
    current = forecast.currently()
    if "Rain" not in current.summary:
        list.append(emojify(":sunny: It's Not Raining :sunny:"))
    else:
        list.append(emojify(":umbrella: It's Raining :umbrella:"))

    list.append(json_obj['city'])
    list.append(forecast.minutely().summary)
    list.append(forecast.hourly().summary)
    list.append(forecast.currently().temperature)


    return list

@app.route('/')
def home_page():
    list = get_weather()
    return render_template('index.html', weather = list[0], city = list[1], current = list[2], day = list[3], temp = list[4])

if __name__ == '__main__':
	#app.run()
    port= int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)