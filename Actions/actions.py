from VoiceRecognition.nlu.Watson import Watson
from equations import listToHyphenString
from equations import preprocessed
from equations import custom_math
from launchapp import launch_app
from stocks import get_symbol
from stocks import company_stock
from weather import weather_information
from wiki import wiki_scrape
from spellchecker import SpellChecker
import pyttsx3


class Action:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)
        self.watson = Watson()
        self.spell = SpellChecker()
        self.spell.word_frequency.load_text_file("./resources/spellcheck_dictionary.txt")
        self.spell.export("./my_custom_dictionary.gz", gzipped=True)

    def take_action(self, command: str) -> None:
        print("command before spellcheck:", command)
        command = command.split()
        for idx, word in enumerate(command):
            if self.spell.unknown([word]):
                command[idx] = self.spell.correction(word)
        command = " ".join(command)
        response = self.watson.send_message(command)
        print("command after spellcheck:", command)
        print("response", response)
        try:
            intent = self.watson.get_intents(response)[0]["intent"]
        except IndexError:
            intent = 'default'
        print(intent)
        if intent == "stocks":
            stocks_str = company_stock(command)
            self.say_out_loud(stocks_str)
        elif intent == "Weather":
            weather_str = weather_information(command)
            self.say_out_loud(weather_str)
        elif intent == "wikipedia":
            wiki_str = wiki_scrape(command)
            self.say_out_loud(wiki_str)
            # TODO wiki.py needs work
        elif intent == "math":
            equation_str = custom_math(preprocessed(command))
            self.say_out_loud(equation_str)
        elif intent == 'default':
            self.say_out_loud("I didn't understand. You can try rephrasing.")

    def say_out_loud(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == '__main__':
    action_obj = Action()
    action_obj.take_action("What five times five")
