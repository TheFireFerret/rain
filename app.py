import logging
import os
import forecastio
import requests
import json

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

api_key = "8ac8a9f185a7384bdeae01ec9fadee8f"

#get weather
def get_my_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

def get_weather():
    url = "http://ip-api.com/json/"
#    ip = get_my_ip()
    ip = "2601:602:9804:4396:9523:5bb6:a710:35da"
    #print url+ip
    r = requests.get(url+ip)
    json_string = json.dumps(r.json())
    json_obj = json.loads(json_string)
    print(json_obj['lat'])
    forecast = forecastio.load_forecast(api_key, json_obj['lat'], json_obj['lon'])
    current = forecast.currently()
    if "Rain" not in current.summary:
    	return "no rain"
    else:
    	return "rain"

@app.route('/')
def home_page():
	return render_template('index.html', weather = get_weather())


#@app.route('/room/<string:groupKey>')
#def group_id_path(groupKey):
#	return render_template('room.html', groupKey = groupKey)

if __name__ == '__main__':
	#app.run()
    port= int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)