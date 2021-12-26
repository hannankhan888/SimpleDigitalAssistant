import soundfile as sf
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2FeatureExtractor, Wav2Vec2Tokenizer
import pyctcdecode
import time


class Wave2Vec2Inference():
    def __init__(self,model_name):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = (Wav2Vec2ForCTC.from_pretrained(model_name)).to(self.device)
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)


    def buffer_to_text(self,audio_buffer):
        if(len(audio_buffer)==0):
            return ""

        inputs = self.processor(audio_buffer, sampling_rate=16000, return_tensors="pt").to(self.device)
        with torch.no_grad():
            logits = self.model(inputs.input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        return transcription.lower()

    def file_to_text(self,filename):
        audio_input, samplerate = sf.read(filename)
        assert samplerate == 16000
        return self.buffer_to_text(audio_input)

if __name__ == "__main__":
    print("Model test")
    print(torch.cuda.get_device_name(0))

    asr = Wave2Vec2Inference("facebook/wav2vec2-large-960h")
    text = asr.file_to_text("C:/Users/Ali Abdul-Hameed/PycharmProjects/SimpleDigitalAssistant/resources/augmented_audio_files/noisy_harvard.wav")
    print(text)