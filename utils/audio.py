#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__copyright__ = "Copyright 2022, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__license__ = "MIT"

import librosa
from audiomentations import Compose, AddGaussianNoise, PitchShift, TimeStretch, Shift
from scipy.io.wavfile import write


def get_16k_sampled_audio_arr(path: str, sample_rate: int):
    """:returns a tuple containing the audio array, and the sampling rate."""
    audio_arr, sample_rate = librosa.load(path=path, sr=sample_rate)
    return audio_arr, sample_rate


def get_pitched_audio(audio_arr, sample_rate, pitch_factors):
    """Shifts the audio array by the given list of pitch_factors.

    :param audio_arr: a numpy array of 16K sampled audio.
    :param sample_rate: the sample rate to use for the pitch_outputs.
    :param pitch_factors: a list of floats containing the n_steps to pitch
    the audio array by.

    :returns pitch_outputs: A list containing the pitch_shifted numpy arrays."""

    pitch_outputs = []
    for pitch_factor in pitch_factors:
        pitch_outputs.append(librosa.effects.pitch_shift(audio_arr, sample_rate, pitch_factor))

    return pitch_outputs


def get_time_stretched_audio(audio_arr, time_stretch_factors):
    """Stretches the audio array by the given list of time_stretch_factors. A factor
    <=1 will slow down the audio. A factor >=1 will speed up the audio.

    :param audio_arr: a numpy array of 16K sampled audio.
    :param time_stretch_factors: a list of floats containing the rates to stretch the
    audio_arr by. (either to slow or speed up).

    :returns time_stretch_outputs: A list containing the time_stretched numpy arrays."""

    time_stretch_outputs = []
    for time_stretch_factor in time_stretch_factors:
        time_stretch_outputs.append(librosa.effects.time_stretch(audio_arr, time_stretch_factor))

    return time_stretch_outputs


def augment_audio_file(path, sample_rate) -> ():
    """Augments an audio .wav file. There is a parameter p which represents the
    probability with which a transformation will be applied. Be sure this is set to 1.

    :param path: file path.
    :param sample_rate: the rate at which the audio file is to be sampled.

    :returns a tuple containing the noisy, pitched, stretched, and shifted arrays.
    """
    # we get the audio arr from the wav file.
    audio_arr, sample_rate = get_16k_sampled_audio_arr(path, sample_rate)

    augment_noise = Compose([
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=1)
    ])
    augment_pitch = Compose([
        PitchShift(min_semitones=1, max_semitones=4, p=1)
    ])
    augment_time_stretch = Compose([
        TimeStretch(min_rate=1.5, max_rate=2, p=1)
    ])
    augment_shift = Compose([
        Shift(min_fraction=-0.5, max_fraction=0.5, p=1)
    ])

    noisy_arr = augment_noise(audio_arr, sample_rate)
    pitched_arr = augment_pitch(audio_arr, sample_rate)
    stretched_arr = augment_time_stretch(audio_arr, sample_rate)
    shifted_arr = augment_shift(audio_arr, sample_rate)

    return noisy_arr, pitched_arr, stretched_arr, shifted_arr


def main():
    path = "../resources/audio_files/harvard.wav"
    output_path = "../resources/augmented_audio_files/"
    sample_rate = 16000

    # we get the audio arr from the wav file.
    # audio_arr, sample_rate = get_16k_sampled_audio_arr(path, 16000)
    # print("audio_arr",audio_arr)
    # we set the factors for pitch and time-stretch augmentation:
    # now we do the computations
    # pitch_outputs = get_pitched_audio(audio_arr, sample_rate, pitch_factors)
    # time_stretch_outputs = get_time_stretched_audio(audio_arr, time_stretch_factors)
    # for i, pitch_output in enumerate(pitch_outputs):
    #     write(output_path + f"pitched_harvard_factor{i + 1}.wav", sample_rate, pitch_output)
    # for i, time_stretch_output in enumerate(time_stretch_outputs):
    #     write(output_path + f"stretched_harvard_factor{i + 1}.wav", sample_rate, time_stretch_output)

    noisy_arr, pitched_arr, stretched_arr, shifted_arr = augment_audio_file(path, sample_rate)
    write(output_path + f"noisy_harvard.wav", sample_rate, noisy_arr)
    write(output_path + f"pitched_harvard.wav", sample_rate, pitched_arr)
    write(output_path + f"stretched_harvard.wav", sample_rate, stretched_arr)
    write(output_path + f"shifted_harvard.wav", sample_rate, shifted_arr)


if __name__ == "__main__":
    main()
