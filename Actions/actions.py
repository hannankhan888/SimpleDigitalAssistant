from VoiceRecognition.nlu.Watson import Watson
from equations import listToHyphenString
from equations import preprocessed
from equations import math
from launchapp import launch_app
from stocks import get_symbol
from stocks import company_stock
from weather import weather_information
from wiki import wiki_scrape
import pyttsx3


class Action:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.watson = Watson()
        self.engine.say("Hello")
        self.engine.runAndWait()

    def take_action(self, command: str) -> None:

        response = self.watson.send_message(command)
        intent = self.watson.get_intents(response)[0]["intent"]
        print(intent)
        if intent == "stocks":
            company_stock(command)
        elif intent == "Weather":
            weather_str = weather_information(command)
            self.say_out_loud(weather_str)
    def say_out_loud(self,text):
        self.engine.say(text)
        self.engine.runAndWait()


action_obj = Action()
action_obj.take_action("Texas weather")
