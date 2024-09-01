import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
API_KEY = '44cc0a6fa71db1f05efafec4c0e619a4'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    weather_data = get_weather(city)
    forecast_data = get_forecast(city)
    forecast_data = filter_daily_forecast(forecast_data)  # Filter for daily forecast
    return render_template('index.html', weather=weather_data, forecast=forecast_data)


@app.route('/geolocation', methods=['POST'])
def geolocation():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    weather_data = get_weather_by_coords(latitude, longitude)
    forecast_data = get_forecast_by_coords(latitude, longitude)
    forecast_data = filter_daily_forecast(forecast_data)  # Filter for daily forecast
    return jsonify({
        'city': weather_data['name'],
        'weather': weather_data,
        'forecast': forecast_data
    })


def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()


def get_forecast(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()


def get_weather_by_coords(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()


def get_forecast_by_coords(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()


def filter_daily_forecast(forecast_data):
    """Filters the forecast data to provide only one entry per day (closest to 12:00)"""
    filtered_forecast = {'list': []}
    seen_dates = set()

    for item in forecast_data['list']:
        date = item['dt_txt'].split(' ')[0]
        time = item['dt_txt'].split(' ')[1]

        # Pick the forecast closest to 12:00 for each day
        if date not in seen_dates and time == '12:00:00':
            filtered_forecast['list'].append(item)
            seen_dates.add(date)

    return filtered_forecast


if __name__ == '__main__':
    app.run(debug=True)
