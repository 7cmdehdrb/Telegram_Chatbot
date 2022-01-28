import sys
import os
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET
import json


load_dotenv(verbose=True)

TOKEN = os.getenv("WEATHER_API_KEY")


class Weather:
    class Wind:
        def __init__(self, speed, direction):
            self.speed = speed
            self.direction = direction

            self.redefineWind()

        def redefineWind(self):
            if self.speed is None:
                self.speed = "정보없음"
                self.direction = "정보없음"

        def createText(self):
            text = ""
            text += "풍속 : "
            text += str(self.speed) + "\n"
            text += "풍향 : "
            text += str(self.direction) + "\n"

            return text

    def __init__(self, weather, temp, temp_min, temp_max, wind):
        # Initialize
        self.weather = weather
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.wind = wind

        # Control Data
        self.redefineWeather()

    def redefineWeather(self):
        if self.weather is None:
            self.weather = "정보없음"
            self.temp = "정보없음"
            self.temp_min = "정보없음"
            self.temp_max = "정보없음"

    def printData(self):
        print(self.weather, self.temp, self.temp_min, self.temp_max)

    def createText(self):
        text = ""
        text += "현재 날씨 : "
        text += str(self.weather) + "\n"
        text += "현재 기온 : "
        text += str(self.temp) + "\n"
        text += "최고 기온 : "
        text += str(self.temp_max) + "\n"
        text += "최저 기온 : "
        text += str(self.temp_min) + "\n"
        text += self.wind.createText()

        return text


def getWeatherXML(city: str):
    # XML

    # Initialize
    weather = temperature = temp_min = temp_max = speed = direction = None

    # HTTP requests

    URL = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": TOKEN,
        "mode": "xml",
        "units": "metric",
        "lang": "kr",
    }

    res = requests.get(url=URL, params=params)
    text = res.text

    # parse XML

    xtree = ET.fromstring(text)

    for node in xtree:
        # <weather number="800" value="맑음" icon="01d"></weather>
        if node.tag == "weather":
            weather = node.attrib["value"]  # "맑음"

        # <temperature value="1.62" min="-0.31" max="3.66" unit="celsius"></temperature>
        elif node.tag == "temperature":
            temperature = node.attrib["value"]  # "1.62"
            temp_min = node.attrib["min"]  # "-0.31"
            temp_max = node.attrib["max"]  # "3.66"

        # <wind> ... </wind>
        elif node.tag == "wind":
            for n in node:
                # <speed value="5.66" unit="m/s" name="Moderate breeze"></speed>
                if n.tag == "speed":
                    speed = n.attrib["value"]  # "5.66"

                # <direction value="260" code="W" name="West"></direction>
                elif n.tag == "direction":
                    direction = n.attrib["value"]  # "260"

            wind = Weather.Wind(speed, direction)

    wt = Weather(
        weather=weather,
        temp=temperature,
        temp_min=temp_min,
        temp_max=temp_max,
        wind=wind,
    )

    # print(weather, temperature, temp_min, temp_max)

    return wt


def getWeatherJSON(city: str):
    # JSON

    # Initialize
    weather = temperature = temp_min = temp_max = speed = direction = None

    # HTTP requests

    URL = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": TOKEN,
        "mode": "json",
        "units": "metric",
        "lang": "kr",
    }

    res = requests.get(url=URL, params=params)
    text = res.text
    json_data = json.loads(text)

    """

        JSON DATA EXAMPLE

      "weather": [
        { "id": 800, "main": "Clear", "description": "맑음", "icon": "01n" }
        ],
        "main": {
            "temp": -1.59,
            "feels_like": -4.39,
            "temp_min": -3.29,
            "temp_max": -0.34,
            "pressure": 1023,
            "humidity": 47
        },
        "wind": { "speed": 2.06, "deg": 270 },
    """

    weather = json_data["weather"][0]["description"]

    temp = json_data["main"]
    temperature = temp["temp"]
    temp_max = temp["temp_max"]
    temp_min = temp["temp_min"]

    wind = json_data["wind"]
    speed = wind["speed"]
    direction = wind["deg"]

    wind = Weather.Wind(speed=speed, direction=direction)
    wt = Weather(
        weather=weather,
        temp=temperature,
        temp_min=temp_min,
        temp_max=temp_max,
        wind=wind,
    )

    # print(weather, temperature, temp_min, temp_max, speed, direction)

    return wt
