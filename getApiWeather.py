from flask import Blueprint
from flask import render_template
import requests
import datetime

weatherAPI = Blueprint('weatherAPI', __name__)

@weatherAPI.route('/weather',methods = ['POST', 'GET'])
def weather():
    dataWeather = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Zaporozhye?unitGroup=metric&key=G8GP3VDB66XR9WCHZ64UCRVNP&contentType=json')
    today = datetime.datetime.today()

    print( today.strftime("%Y-%m-%d") ) # %Y-%m-%d
    todayTime = today.strftime("%Y-%m-%d")

    print(f'сегодня {todayTime} температура в Запорожье: ',dataWeather.json()['days'][0]['temp'])
    tomorrow = today + datetime.timedelta(days=1)

    print(f'завтра {tomorrow.date()} температура в Запорожье: ',dataWeather.json()['days'][1]['temp'])
    return render_template('weather.html', todayTime=today.strftime("%Y-%m-%d"), forecastToday=dataWeather.json()['days'][0]['temp'], forecastTomorrow=dataWeather.json()['days'][1]['temp'])