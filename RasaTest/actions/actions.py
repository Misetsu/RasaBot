from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from .data import eng
import requests


class ActionSetAlarm(Action):

    def name(self) -> Text:
        return "action_set_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.slots["set_time"]
        dispatcher.utter_message(text="OK、{}にセットした。".format(time))

        return []


class ActionCheckWeather(Action):

    def name(self) -> Text:
        return "action_check_weather"

    def run(self, dispatcher, tracker, domain):
        name = tracker.get_slot("location")
        city = eng(name)
        api_token = "e6d4ad10365893af3727a5ccb4aa4028"
        url = "https://api.openweathermap.org/data/2.5/weather"
        payload = {"q": city, "appid": api_token, "units": "metric", "lang": "ja"}
        response = requests.get(url, params=payload)
        weather_data = response.json()
        if weather_data["cod"] != "404":
            city = weather_data["name"]
            description = weather_data["weather"][0]["description"]
            temp = weather_data["main"]["temp"]
            max_temp = weather_data["main"]["temp_max"]
            min_temp = weather_data["main"]["temp_min"]
            msg = f"今日{city}の天気は{description}。今の気温は{temp}度。最高気温は{max_temp}度、そして最低気温は{min_temp}度。"
        else:
            msg = "その場所が見つかんない。"
        dispatcher.utter_message(msg)

        return [SlotSet("location", None)]
