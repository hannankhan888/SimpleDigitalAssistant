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
        self._init_spell_checker()

    def _init_spell_checker(self):
        self.spell.word_frequency.load_text_file("./resources/spellcheck_dictionary.txt")
        with open("resources/words_to_remove_from_dictionary.txt", 'r') as file:
            self.spell.word_frequency.remove(file.readline().strip(" \n"))
        # self.spell.export("./my_custom_dictionary.gz", gzipped=True)

    def take_action(self, command: str) -> None:
        result_str = ""
        intent = "default"
        confidence = 0
        print("command before spellcheck:", command)
        command = self.spell_check(command)
        response = self.watson.send_message(command)
        print("command after spellcheck:", command)
        # print("response", response)
        try:
            intent = self.watson.get_intents(response)[0]["intent"]
            confidence = self.watson.get_intents(response)[0]['confidence']
        except IndexError:
            intent = 'default'
        print("intent:", intent)
        print("confidence:", confidence)
        if confidence > 0.30:
            if intent == "stocks":
                result_str = company_stock(command)
            elif intent == "Weather":
                result_str = weather_information(command)
            elif intent == "wikipedia":
                result_str = wiki_scrape(command)
                # TODO wiki.py needs work
            elif intent == "math":
                result_str = custom_math(preprocessed(command))
            elif intent == 'default':
                result_str = "I didn't understand. You can try rephrasing."
        else:
            result_str = "I didn't understand. You can try rephrasing."

        self.say_out_loud(result_str)

    def spell_check(self, command: str) -> str:
        """:returns The command string after it has been spellchecked."""

        command = command.split()

        for idx, word in enumerate(command):
            if self.spell.unknown([word]):
                command[idx] = self.spell.correction(word)

        return " ".join(command)

    def say_out_loud(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == '__main__':
    action_obj = Action()
    action_obj.take_action("What five times five")
