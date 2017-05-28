import os
from collections import namedtuple
import time

import requests

from filters import regular_intervals

forecast_url = 'https://api.darksky.net/forecast/{0}/{1},{2}'

ForecastData = namedtuple('forecastdata', 'time temperature tempMin, tempMax, pressure chancePrecip precipIntensity windBearing windSpeed')

def forecast_request(key, lat, lng):
    r = requests.get(forecast_url.format(key,lat,lng))
    return r.json()

def forecast_decode(forecast):
    return ForecastData(forecast.get('time'),
                        forecast.get('temperature'),
                        forecast.get('temperatureMin'),
                        forecast.get('temperatureMax'),
                        forecast.get('pressure'),
                        forecast.get('precipProbability'),
                        forecast.get('precipIntensity'),
                        forecast.get('windBearing'),
                        forecast.get('windSpeed'))

def forecast_to_sequence(forecast):
    yield forecast_decode(forecast['currently'])
    for h in forecast['hourly']['data']:
        yield forecast_decode(h)
    for d in forecast['daily']['data']:
        yield forecast_decode(d)

def weather_route_data (parser):
    weather = []
    key = os.environ['FORECAST_API_KEY']

    for p in regular_intervals(parser.points_with_attributes(), 10):
        forecast = forecast_request(key, p['lat'], p['lon'])
        weather.append(list(forecast_to_sequence(forecast)))
    return weather

def forecast_at_time(forecast, t):
    f = min(forecast, key=lambda x: abs(x.time - t))
    return f

def weather_route_now(parser):
    now = int(time.time())
    weather = weather_route_data(parser);
    for w in weather:
        f = forecast_at_time(w, now)
        print(f)
    
