import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'C:\\Users\\Ali Abdul-Hameed\\PycharmProjects\\SimpleDigitalAssistant\\VoiceRecognition\\nlu')
from Watson import Watson

nlu = Watson()

response = nlu.send_message("What is the weather in Canada")
print(nlu.get_intents(response))

