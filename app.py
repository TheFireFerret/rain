import logging
import os
import forecastio
import requests
import json
import emoji

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

    list = []

    r = requests.get(url+ip)
    json_string = json.dumps(r.json())
    json_obj = json.loads(json_string)

    if json_obj['status'] == "fail" :
        return [url+ip, emoji.emojize('Something went wrong :thumbs_down_sign:')]

    forecast = forecastio.load_forecast(api_key, json_obj['lat'], json_obj['lon'])
    current = forecast.currently()
    if "Rain" not in current.summary:
        list.append(emoji.emojize("It's Not Raining :sunny:"))
    else:
        list.append(emoji.emojize("It's Raining :umbrella:"))

    list.append(json_obj['city'])
    return list

@app.route('/')
def home_page():
	return render_template('index.html', weather = get_weather()[0], city = get_weather()[1])


#@app.route('/room/<string:groupKey>')
#def group_id_path(groupKey):
#	return render_template('room.html', groupKey = groupKey)

if __name__ == '__main__':
	#app.run()
    port= int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)