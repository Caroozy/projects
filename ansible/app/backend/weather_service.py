import datetime
from http.client import responses
import re
import requests
from deep_translator import GoogleTranslator
from backend import objects


def get_weather(usr_input, cache):
    """
        checks if location exists in cache by user input,
        if exists return in,
        if nonexistent search in

    :return: week() | None
    """

    def __init_week(json_file):
        """
            creating a week object out of a  week forecast api

        :param json_file: [requests].get handled json response
        :return: None | Week()
        """
        word = json_file['resolvedAddress']
        if re.search('^[a-zA-Z ,]*$', word) is None:
            word = GoogleTranslator(src='auto', dest='en').translate(word)

        location = word.replace(' ', '-')
        location = location.lower()

        days = []
        for day in json_file['days']:  # unpack days and average hours in day
            sunset_hour = day['sunset'][:2]
            temp_day = []
            temp_night = []
            date = day['datetime']

            for hour in day['hours']:
                hour_num = hour['datetime'][:2]
                if hour_num[0] == '0':
                    hour_num = hour_num[1:2]

                if 4 <= int(hour_num) <= int(sunset_hour):  # 4AM seems like a good hour to start recording day average
                    temp_day.append(float(hour['temp']))
                elif int(sunset_hour) < int(hour_num):
                    temp_night.append(float(hour['temp']))

            avg_day = float(str(sum(temp_day) / len(temp_day))[:4])
            avg_night = float(str(sum(temp_night) / len(temp_night))[:4])
            humidity = day['humidity']

            day = objects.DayWeather(avg_day, avg_night, humidity, date)
            days.append(day)

        cache.write_week(objects.WeekWeather(days, location))

        return objects.WeekWeather(days, location.replace('-', ' '))

    key_weather_visualcrossing_com = os.getenv('WEATHER_KEY')
    params = {
        'key': key_weather_visualcrossing_com,
        'unitGroup': 'metric',
        'include': 'days,hours,datetime',
        'elements': 'resolvedAddress,datetime,temp,humidity,sunset,sunrise',
        'lang': 'en'
    }
    get = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{usr_input}/next6days'

    val = cache.is_exist(usr_input)

    def get_req():
        with requests.get(get, params=params) as response:

            print(f'Server GET response status: {response.status_code}')
            print(responses[response.status_code])

            if int(response.status_code) != 200:
                return None

            response = response.json()
            week_init = __init_week(response)

            return week_init

    if val is False:  # if location not in cache
        return get_req()
    else:
        week = cache.get_week(val)  # get week from cache and send unpacked
        week_obj = objects.unpack_week_from_cache(week)
        week_date = week_obj.get_days()[0].get_date()

        if week_date != str(datetime.date.today()):
            cache.cleanup()
            return get_req()

        print(f'Valid week forecast pulled from cache')
        return week_obj
