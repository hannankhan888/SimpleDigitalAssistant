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
        self.engine.say("I will speak this text")
        self.engine.runAndWait()

    def take_action(self, command: str) -> None:
        # TODO: retrieve intent from Watson.
        intent = "math"

        response = self.watson.send_message(command)
        intent = self.watson.get_intents(response)[0]["intent"]
        print(intent)


action_obj = Action()
action_obj.take_action("what is the current price of apple stock")
