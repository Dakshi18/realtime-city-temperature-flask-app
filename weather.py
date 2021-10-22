from os import environ
from requests import get


class weather:
    def get_weather(city):

        API_KEY = environ.get('API_KEY')

        loc_id=get("http://dataservice.accuweather.com/locations/v1/cities/search?apikey={}&q={}".format(API_KEY,city)).json()
        loc_id = loc_id[0]['Key']
        print(loc_id)

        weather_result=get("http://dataservice.accuweather.com/currentconditions/v1/{}?apikey={}&details=true".format(loc_id,API_KEY)).json()
        for w in weather_result:
            temperature = w['Temperature']['Metric']['Value'] 

        return temperature





