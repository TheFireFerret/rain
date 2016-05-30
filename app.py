import logging
import os
import forecastio
import requests
import json

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

api_key = "8ac8a9f185a7384bdeae01ec9fadee8f"

#get weather

def get_weather():
    url = "http://ip-api.com/json/"
    ip = request.remote_addr
#    ip = "2601:602:9804:4396:9523:5bb6:a710:35da"
    print url+ip
#    print request.remote_addr

    list = []

    r = requests.get(url+ip)
    json_string = json.dumps(r.json())
    json_obj = json.loads(json_string)
    print json_string
    if json_obj['status'] == "fail" :
        return [url+ip, url+ip]
    forecast = forecastio.load_forecast(api_key, json_obj['lat'], json_obj['lon'])
    current = forecast.currently()
    if "Rain" not in current.summary:
        list.append("no rain")
    #	return "no rain"
    else:
        list.append("rain")
    #	return "rain"

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