#Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный момент для города, название которого получается через input. https://openweathermap.org/current

from pprint import pprint
import requests
import json

API_key = 'enter here API key'

def weather(API_key):
    city_name = str(input('Введите город на русском языке:'))
    lang = 'ru'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&lang={lang}'
    response = json.loads((requests.get(url)).text)
    return pprint(response)