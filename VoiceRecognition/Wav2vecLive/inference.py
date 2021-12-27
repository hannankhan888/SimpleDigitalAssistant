import time
import soundfile as sf
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from pyctcdecode import build_ctcdecoder
from tqdm import tqdm

# for testing
from datasets import load_dataset, load_metric
import re

class Wave2Vec2Inference():
    def __init__(self, model_name, lm_path=None):
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        except:
            self.device = torch.device("cpu")
        self.model = (Wav2Vec2ForCTC.from_pretrained(model_name)).to(self.device)
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        vocab_dict = self.processor.tokenizer.get_vocab()
        sorted_dict = {k.lower(): v for k, v in sorted(vocab_dict.items(), key=lambda item: item[1])}
        if lm_path:
            alpha=0
            beta=0
            beam_width = 1024
            self.decoder = build_ctcdecoder(list(sorted_dict.keys()), lm_path)
        else:
            self.decoder = None


    def buffer_to_text(self, audio_buffer):
        if(len(audio_buffer)==0):
            return ""

        inputs = self.processor(audio_buffer, sampling_rate=16000, return_tensors="pt").to(self.device)

        if self.decoder:
            with torch.no_grad():
                logits = self.model(inputs.input_values).logits.numpy()[0]
            transcription = self.decoder.decode(logits)
        else:
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
    MODELS = {
        "large": "facebook/wav2vec2-large-960h",
        "distil": "OthmaneJ/distil-wav2vec2"
    }
    LM = "VoiceRecognition/4gram_big.arpa"
    asr = Wave2Vec2Inference(model_name=MODELS["small"],lm_path=LM)
    text = asr.file_to_text("resources/augmented_audio_files/noisy_harvard.wav")
    print(text)