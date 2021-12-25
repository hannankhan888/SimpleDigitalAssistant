import soundfile as sf
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

class Wave2Vec2Inference():
    def __init__(self,model_name):
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)

    def buffer_to_text(self,audio_buffer):
        if(len(audio_buffer)==0):
            return ""

        inputs = self.processor(audio_buffer, sampling_rate=16000, return_tensors="pt")

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
    asr = Wave2Vec2Inference("jonatasgrosman/wav2vec2-large-xlsr-53-english")
    text = asr.file_to_text("scripts/harvard_new.wav")
    print(text)