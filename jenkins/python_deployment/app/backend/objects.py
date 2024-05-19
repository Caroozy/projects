import ast
import datetime
import os.path
import pandas as pd


# add father class and make protected
def unpack_week_from_cache(week):
    """
        unpacking dict from cache returning a week object with location name and

    :param week: dict - resembling a week
    :return: week_w() - an object resembling a week
    """
    days_list = week['days']
    location = week['location'].replace('-', ' ')

    days_obj = []
    for day in days_list:
        days_obj.append(unpack_day_from_cache(day))

    return WeekWeather(days_obj, location)


def unpack_day_from_cache(day):
    """
        unpacking day dictionary

    :param day:
    :return:
    """
    d_tmp = day['temp_day']
    n_tmp = day['temp_night']
    humid = day['humidity']
    date = day['date']
    return DayWeather(d_tmp, n_tmp, humid, date)


class DayWeather:

    def __init__(self, temp_d: float, temp_n: float, humid: float, date: str):
        self.__temp_d = temp_d
        self.__temp_n = temp_n
        self.__humid = humid
        self.__date = date

    def get_date(self):
        return self.__date

    def get_day_temp(self):
        return self.__temp_d

    def get_night_temp(self):
        return self.__temp_n

    def get_humidity(self):
        return self.__humid

    def get_day_week(self):
        date = datetime.datetime.strptime(self.__date, '%Y-%m-%d').date()
        return date.strftime('%A')

    def pack_day_to_cache(self):
        return {
            'temp_day': self.__temp_d,
            'temp_night': self.__temp_n,
            'humidity': self.__humid,
            'date': self.__date
        }

    def __str__(self):
        date = datetime.datetime.strptime(self.__date, '%Y-%m-%d').date()

        return (f"\ndate: {self.__date}\n"
                + f"{date.strftime('%A')}\n"
                + f"average day temp: {self.__temp_d}\n"
                + f"average night temp: {self.__temp_n}\n"
                + f"humidity %{self.__humid}\n")


class WeekWeather:

    def __init__(self, days: list, location: str):
        self.__days = days
        self.__location = location

    def get_days(self):
        return self.__days

    def get_location(self):
        return self.__location

    def pack_week_to_cache(self):
        day_dict = []
        for day in self.__days:
            day = day.pack_day_to_cache()
            day_dict.append(day)

        return {
            'days': day_dict,
            'location': self.__location
        }

    def __str__(self):

        days_str = ''
        for day in self.__days:
            days_str += str(day)

        return (f"Location:\n"
                + f"{self.__location}\n"
                + f"days[\n"
                + f"{days_str}"
                + f"\n]")


class Cache:

    """
        A cache instance can write weeks to the hidden csv file kept on root folder,
        write week: writes to cache
        cleanup: cleans
    """

    def __init__(self):
        self.__expiration = 2
        self.__cache_path = './.week_storage_weather.csv'
        self.__last_cleanup = datetime.datetime.now()
        self.cleanup()

    def write_week(self, week: WeekWeather):
        """
            writing to db creating new file on root app folder if nonexistent

        :param week:
        :return: None
        """
        week_packed = week.pack_week_to_cache()
        df = pd.json_normalize(week_packed)
        if os.path.exists(self.__cache_path):
            df.to_csv(self.__cache_path, mode='a', index=False, header=False)
            return
        df.to_csv(self.__cache_path, mode='w', index=False, header=True)

    def cleanup(self):
        """
            scanning dates deleting all different from today
        :return: None
        """
        if not os.path.exists(self.__cache_path):
            return
        df = pd.read_csv(self.__cache_path, converters={'days': ast.literal_eval})
        rem_list = []
        weeks = df.to_dict()
        index = 0
        for week in weeks['days'].values():
            for day in week:
                date = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
                if datetime.date.today() != date.date():
                    rem_list.append(index)
                index += 1
                break

        df = df.drop(index=rem_list)  # dropping from DataFrame()
        df.to_csv(self.__cache_path, mode='w', header=True, index=False)  # rewriting csv file
        self.__last_cleanup = datetime.datetime.now()

    def is_exist(self, location):
        if not os.path.exists(self.__cache_path):
            return False
        elif location is None:
            return False

        time_diff = datetime.datetime.now() - self.__last_cleanup

        df = pd.read_csv(self.__cache_path, converters={'days': ast.literal_eval})  # converting csv file to DataFrame
        location = location.replace(' ', '-')                                       # ast.literal_eval is converting
        city_reg = f'{location}[-,].*'                                              # a string into object by represent
        country_reg = f'^{location}$'
        index = df[df['location'].str.contains(city_reg, na=False)].index
        if len(index) > 0:
            return index[0]
        index = df[df['location'].str.contains(country_reg)].index
        if len(index) > 0:
            return index[0]

        return False

    def get_week(self, index):
        """
            returns DataFrame row
        :param index: index row
        :return: DataFrame row
        """
        df = pd.read_csv(self.__cache_path, converters={'days': ast.literal_eval})
        return df.loc[index]
