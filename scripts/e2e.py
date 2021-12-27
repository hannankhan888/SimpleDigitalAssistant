import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'VoiceRecognition/nlu')
import Watson

nlu = Watson.Watson()

response = nlu.send_message("What is five time five times four")
intent_list = nlu.get_intents(response)
if intent_list[0]["intent"] == "math":
    print("this is a math equation")

