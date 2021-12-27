import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'VoiceRecognition/nlu')
import Watson

nlu = Watson.Watson()

response = nlu.send_message("What is five time five times four")
print(nlu.get_intents(response))

