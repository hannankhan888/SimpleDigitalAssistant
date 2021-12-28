FROM pytorch/pytorch

# install utilities
RUN apt update && \
    apt install vim net-tools ffmpeg portaudio19-dev \
    alsa-base alsa-utils \
    libportaudio2 libportaudiocpp0 libsndfile1-dev \
    -y

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    jupyter 

# Copy our application code
WORKDIR /workspace

# . Here means current directory.
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "./VoiceRecognition/Wav2vecLive/inference.py"]