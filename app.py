#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This file contains the GUI for the SimpleDigitalAssistant application.
    This application is made specifically for Windows OS, and can be used
    to accomplish small tasks via voice recognition (using pre-trained models)."""

__author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__copyright__ = "Copyright 2021, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Hannan Khan"
__email__ = "hannankhan888@gmail.com"

import sys
import threading

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont, QFontDatabase, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QFrame, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from utils.dynamicPyQt5Labels import CustomButton
from utils.dynamicPyQt5Labels import ImageChangingLabel, ImageBackgroundChangingLabel
from utils.framelessDialogs import FramelessMessageDialog, FramelessScrollableMessageDialog
import pyaudio
import numpy as np
import sounddevice as sd
from VoiceRecognition.Wav2vecLive.realTimeAudio import LiveWav2Vec2
from VoiceRecognition.Wav2vecLive.inference import Wave2Vec2Inference

CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000
NUMPY_DATATYPE = np.int16


class RootWindow(QMainWindow):
    """ This class is the main window of our application. It creates and calls an
    inference object Wave2Vec2Inference which uses a pretrained model to achieve
    automatic speech recognition."""

    def __init__(self, model_name):
        super(RootWindow, self).__init__()

        self.WIDTH = 1024
        self.HEIGHT = 576
        self.app_name = "SimpleDigitalAssistant"
        self.mousePressPos = None
        self.mouseMovePos = None
        self.listening_for_max = False
        self.recording = False
        self.p = None
        self.stream = None
        self.buffer = []
        self.np_buffer = None
        self.threads = []
        self.recording_thread = None
        self.listening_for_max_thread = None
        self.asr_print_thread = None
        self.model_name = model_name
        self.wav2vec_inference = Wave2Vec2Inference(self.model_name)

        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)

        # opens the window in the middle of the screen.
        self.qtRectangle = self.frameGeometry()
        self.centerPoint = QDesktopWidget().availableGeometry().center()
        self.qtRectangle.moveCenter(self.centerPoint)
        self.move(self.qtRectangle.topLeft())

        # create a Frameless window
        self.setWindowFlags(Qt.FramelessWindowHint)

        # create a font database, and load the custom Lato-Thin font
        self.font_database = QFontDatabase()
        self.lato_font_id = self.font_database.addApplicationFont("resources/fonts/Lato-Light.ttf")
        self.lato_font_family = self.font_database.applicationFontFamilies(self.lato_font_id).__getitem__(0)
        self.current_font = QFont(self.lato_font_family, 20)

        # create a main frame for overall layout
        self.main_frame = QFrame()
        self.main_frame_stylesheet = """
        QFrame {background-color: rgb(255, 232, 214)}
        """
        self.main_frame.setStyleSheet(self.main_frame_stylesheet)

        self.main_frame_layout = QVBoxLayout()
        self.main_frame_layout.setSpacing(0)
        self.main_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.main_frame_layout.setAlignment(Qt.AlignTop)

        self._init_colors()
        self._init_sound_devices()
        self._init_bottom_main_frame()
        self._init_window_frame()

        self.main_frame_layout.addWidget(self.bottom_main_frame)
        self.main_frame.setLayout(self.main_frame_layout)

        self.setCentralWidget(self.main_frame)
        self.start_listening_for_max_thread()
        self.show()

    def _init_bottom_main_frame(self) -> None:
        self.bottom_main_frame = QFrame()
        self.bottom_main_frame_layout = QHBoxLayout()
        self.bottom_main_frame_layout.setSpacing(50)
        self.bottom_main_frame_layout.setContentsMargins(10, 70, 10, 10)
        self.bottom_main_frame_layout.setAlignment(Qt.AlignLeft)

        self.bottom_left_main_frame = QFrame()
        self.bottom_left_main_frame_layout = QVBoxLayout()
        self.bottom_left_main_frame_layout.setSpacing(50)
        self.bottom_left_main_frame_layout.setContentsMargins(10, 10, 10, 10)
        self.bottom_left_main_frame_layout.setAlignment(Qt.AlignCenter)

        self.welcome_label = QLabel()
        self.welcome_label.setFont(self.current_font)
        self.welcome_label.setStyleSheet("""
        QLabel { rgb (88, 105, 126); }
        """)
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setText("Welcome to your digital assistant, MAX!")

        self.output_label = QtWidgets.QTextEdit()
        self.output_label.setReadOnly(True)
        self.output_label.setFont(QFont(self.lato_font_family, 10))
        self.output_label.setTextInteractionFlags(Qt.NoTextInteraction)
        self.output_label.setCursor(QCursor(Qt.ArrowCursor))

        self.mic_label = ImageChangingLabel("resources/images/mic_normal_icon.png",
                                            "resources/images/mic_highlight_icon.png", self._start_recording_thread,
                                            350, 350)

        self.bottom_left_main_frame_layout.addWidget(self.welcome_label)
        self.bottom_left_main_frame_layout.addWidget(self.output_label)
        self.bottom_left_main_frame.setLayout(self.bottom_left_main_frame_layout)
        self.bottom_main_frame_layout.addWidget(self.bottom_left_main_frame)
        self.bottom_main_frame_layout.addWidget(self.mic_label)
        self.bottom_main_frame.setLayout(self.bottom_main_frame_layout)

    def _init_sound_devices(self) -> None:
        self.p = pyaudio.PyAudio()
        self.input_device_dict = pyaudio.PyAudio.get_default_input_device_info(self.p)
        self.input_device_idx = self.input_device_dict['index']
        self.input_device_name = self.input_device_dict["name"]
        self.input_channels = self.input_device_dict['maxInputChannels']
        self.default_sample_rate = self.input_device_dict['defaultSampleRate']

        self.output_device_dict = pyaudio.PyAudio.get_default_output_device_info(self.p)
        self.output_device_num = self.output_device_dict['index']
        self.output_device_name = self.output_device_dict["name"]

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mousePressPos = None
        self.mouseMovePos = None
        if (a0.button() == Qt.LeftButton) and self.window_frame.underMouse():
            self.mousePressPos = a0.globalPos()
            self.mouseMovePos = a0.globalPos()
        super(RootWindow, self).mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if (a0.buttons() == Qt.LeftButton) and (self.window_frame.underMouse()):
            curr_pos = self.pos()
            global_pos = a0.globalPos()
            diff = global_pos - self.mouseMovePos
            new_pos = curr_pos + diff
            self.move(new_pos)
            self.mouseMovePos = global_pos
        super(RootWindow, self).mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        super(RootWindow, self).mouseReleaseEvent(a0)

    def _init_colors(self) -> None:
        # Champagne Pink
        self.normal_bg = QtGui.QColor()
        self.normal_bg.setRgb(255, 232, 214)

        # Macaroni and Cheese
        self.highlight_bg = QtGui.QColor()
        self.highlight_bg.setRgb(255, 186, 133)

        # Dark Electric Blue
        self.normal_color = QtGui.QColor()
        self.normal_color.setRgb(88, 105, 126)

        # Cadet Grey
        self.highlight_color = QtGui.QColor()
        self.highlight_color.setRgb(141, 157, 175)

        # Grey (american silver) color for minimize button
        self.minimize_button_label_highlight_bg = QtGui.QColor()
        self.minimize_button_label_highlight_bg.setRgb(229, 229, 229)

        # Red Color for close button
        self.close_button_label_highlight_bg = QtGui.QColor()
        self.close_button_label_highlight_bg.setRgb(255, 87, 51)

        # White color (champagne flute) for close button when highlighted
        self.close_button_label_highlight_color = QtGui.QColor()
        self.close_button_label_highlight_color.setRgb(246, 234, 226)

    def _init_window_frame(self) -> None:
        self.window_frame = QtWidgets.QFrame()
        self.window_frame.setFixedHeight(60)
        """ Window_frame will have two sub frames, one for the left half, includes the
        icon and name, and one for the right half, includes the close and minimize
        buttons."""
        self.window_frame_layout = QtWidgets.QHBoxLayout()
        self.window_frame_layout.setSpacing(0)
        self.window_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.window_frame_left = QtWidgets.QFrame()
        self.window_frame_right = QtWidgets.QFrame()

        self.wf_left_layout = QtWidgets.QHBoxLayout()
        self.wf_left_layout.setSpacing(0)
        self.wf_left_layout.setContentsMargins(8, 0, 0, 0)
        self.wf_left_layout.setAlignment(Qt.AlignLeft)
        self.wf_right_layout = QtWidgets.QHBoxLayout()
        self.wf_right_layout.setSpacing(0)
        self.wf_right_layout.setContentsMargins(0, 0, 0, 0)
        self.wf_right_layout.setAlignment(Qt.AlignRight)

        self.app_name_label = CustomButton(self.about, self.normal_bg, self.minimize_button_label_highlight_bg,
                                           self.normal_color, self.highlight_color)
        self.app_name_label.setToolTip("About")
        self.app_name_label.setText(self.app_name)
        self.app_name_label.setFont(QFont(self.lato_font_family, 10))
        self.wf_left_layout.addWidget(self.app_name_label)

        self.settings_button_label = ImageBackgroundChangingLabel(self.normal_bg,
                                                                  self.minimize_button_label_highlight_bg,
                                                                  "resources/images/settings_normal_icon.png",
                                                                  "resources/images/settings_highlight_icon.png",
                                                                  self.settings, 30, 60)
        self.settings_button_label.setToolTip("Settings")
        self.settings_button_label.setContentsMargins(0, 0, 5, 0)
        self.wf_right_layout.addWidget(self.settings_button_label)

        self.minimize_button_label = CustomButton(self.minimize_app, self.normal_bg,
                                                  self.minimize_button_label_highlight_bg, self.normal_color,
                                                  self.highlight_color)
        self.minimize_button_label.setToolTip("Minimize")
        self.minimize_button_label.setText("  _  ")
        self.minimize_button_label.setFont(QFont(self.lato_font_family, 10))
        self.wf_right_layout.addWidget(self.minimize_button_label)

        self.close_button_label = CustomButton(self.exit_app, self.normal_bg, self.close_button_label_highlight_bg,
                                               self.normal_color, self.close_button_label_highlight_color)
        self.close_button_label.setToolTip("Close")
        self.close_button_label.setText("   /   ")
        self.close_button_label.setFont(QFont(self.lato_font_family, 10))
        self.wf_right_layout.addWidget(self.close_button_label)

        self.window_frame_left.setLayout(self.wf_left_layout)
        self.window_frame_right.setLayout(self.wf_right_layout)

        self.window_frame_layout.addWidget(self.window_frame_left)
        self.window_frame_layout.addWidget(self.window_frame_right)

        self.window_frame.setLayout(self.window_frame_layout)

        self.main_frame_layout.addWidget(self.window_frame)

    def start_listening_for_max_thread(self):
        """ Starts a thread to open a stream and listen for the hotword 'max'.
        When the keyword is detected, the start_recording_thread function will be
        called."""

        self.listening_for_max_thread = threading.Thread(target=self._listen_for_max)
        self.listening_for_max_thread.setDaemon(True)
        self.listening_for_max_thread.setName("listen_for_max_thread")
        self.threads.append(self.listening_for_max_thread)
        self.listening_for_max_thread.start()

    def _listen_for_max(self):
        self.buffer = []
        self.stream = self.p.open(rate=SAMPLE_RATE, channels=CHANNELS, format=SAMPLE_FORMAT,
                                  frames_per_buffer=CHUNK, input=True)
        self.listening_for_max = True

        # data is of class 'bytes' and needs to converted into a numpy array.
        while self.listening_for_max:
            data = self.stream.read(1024)
            self.buffer.append(data)
            print(len(self.buffer))
            if len(self.buffer) > 10:
                self.buffer = self.buffer[-10:]
                transcribed_txt = self._transcribe_buffer_audio()
                if "max" in transcribed_txt:
                    self.output_label.append(transcribed_txt)
                    self.stream.stop_stream()
                    self.stream.close()
                    self._start_recording_thread()
                    self.listening_for_max = False
        return

    def start_asr_thread(self) -> None:
        """ Starts a thread to open a stream (via realTimeAudio.LiveWave2Vec2)
        and keep transcribing voice until a keyboard interrupt."""

        self.asr_print_thread = threading.Thread(target=self._start_asr_printing)
        self.asr_print_thread.setDaemon(True)
        self.asr_print_thread.setName("Recording Thread")
        self.threads.append(self.asr_print_thread)
        self.asr_print_thread.start()

    def _start_asr_printing(self) -> None:
        try:
            while True:
                text, sample_length, inference_time = self.asr.get_last_text()
                self.output_label.append(text)
                self.output_label.moveCursor(QtGui.QTextCursor.End)
                print(f"{sample_length:.3f}s\t{inference_time:.3f}s\t{text}")

        except KeyboardInterrupt:
            self.asr.stop()

    def _start_recording_thread(self) -> None:
        """ Called by the mic label. Starts a thread that opens a pyaudio stream,
        records audio until the mic label is pressed again. After the recording has been
        stopped, the audio buffer is transcribed via the Wave2VecInference model,
        the stream is closed, and the output text is printed.

        There is an option to play the recorded voice back out loud to you (just in case
        for debugging). Simply uncomment the appropriate line in self.get_voice_command."""

        self.mic_label.invert_active_state()
        self.recording_thread = threading.Thread(target=self.get_voice_command)
        self.recording_thread.setDaemon(True)
        self.recording_thread.setName("recording_thread")
        self.threads.append(self.recording_thread)
        self.recording_thread.start()
        print("threads: ", self.threads)

    def get_voice_command(self) -> None:
        if self.recording:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
            self._transcribe_and_print_buffer_audio()
            # self._play_recorded_buffer_audio()
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
            return

        self.buffer = []
        self.stream = self.p.open(rate=SAMPLE_RATE, channels=CHANNELS, format=SAMPLE_FORMAT,
                                  frames_per_buffer=CHUNK, input=True)
        self.recording = True

        # data is of class 'bytes' and needs to converted into a numpy array.
        while self.recording:
            data = self.stream.read(1024)
            self.buffer.append(data)

    def _get_np_buffer(self) -> None:
        """Sets the numpy buffer by converting the bytes object into a numpy array.
        The numpy buffer can then be used for inference.

        We are dividing by 32767 because this operation will convert the buffer into
        a float array (required by the pytorch model). This number is arbitrary and
        controls the amplitude of the audio (dividing by small numbers results in an
        increase in amplitude (loudness), large numbers result in decrease in amplitude
        (not audible to human ear at 500000)). The transcription is not phased by the
        amplitude. Simply converting the buffer to float results in as loud amplitude
        as dividing by 1.0."""

        self.np_buffer = np.frombuffer(b''.join(self.buffer), dtype=NUMPY_DATATYPE) / 32767

    def _play_recorded_buffer_audio(self) -> None:
        """ Debugging function, used to get the buffer, and play it back out loud.
        Also prints the buffer, and its relevant information."""

        self._get_np_buffer()
        print("np_buffer: ", self.np_buffer, "| len:", len(self.np_buffer), "| size in memory (bytes)",
              (self.np_buffer.size * self.np_buffer.itemsize))
        sd.play(self.np_buffer, SAMPLE_RATE)

    def _transcribe_buffer_audio(self) -> str:
        self._get_np_buffer()
        return self.wav2vec_inference.buffer_to_text(self.np_buffer).lower()

    def _transcribe_and_print_buffer_audio(self) -> None:
        """ Transcribes audio based on the given model."""

        self.transcribed_text = self._transcribe_buffer_audio()
        if self.transcribed_text:
            self.output_label.append(self.transcribed_text)
        else:
            self.output_label.append("Please try again.")
        self.output_label.moveCursor(QtGui.QTextCursor.End)

    def about(self) -> None:
        """This function takes care of the about dialog."""

        about_dialog = FramelessMessageDialog(self,
                                              "Created by Hannan Khan, Salman Nazir,\nReza Mohideen, and Ali "
                                              "Abdul-Hameed.",
                                              self.normal_bg, self.minimize_button_label_highlight_bg,
                                              self.normal_color,
                                              self.highlight_color, self.close_button_label_highlight_bg,
                                              self.close_button_label_highlight_color, "About",
                                              QFont(self.lato_font_family, 15))

        github_label = QtWidgets.QLabel()
        github_label.setFont(self.current_font)
        github_label.setText(
            '<a href="https://github.com/hannankhan888/SimpleDigitalAssistant" style="color: rgba(187, 172, 193, '
            '255)">Github</a>')
        github_label.setOpenExternalLinks(True)

        license_label = CustomButton(self.license, self.normal_bg, self.minimize_button_label_highlight_bg,
                                     self.normal_color, self.highlight_color)
        license_label.setFont(self.current_font)
        license_label.setText("License")
        license_label.setCursor(Qt.PointingHandCursor)

        about_dialog.middle_frame_layout.addWidget(github_label)
        about_dialog.middle_frame_layout.addWidget(license_label)
        about_dialog.exec_()

    def settings(self) -> None:
        pass

    def license(self) -> None:
        license_str = """
MIT License

Copyright (c) 2021 Hannan, Salman, Reza, Ali

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE."""
        license_dialog = FramelessScrollableMessageDialog(self, license_str, self.normal_bg,
                                                          self.minimize_button_label_highlight_bg,
                                                          self.normal_color, self.highlight_color,
                                                          self.close_button_label_highlight_bg,
                                                          self.close_button_label_highlight_color, "License",
                                                          QFont(self.lato_font_family, 12))
        license_dialog.exec_()

    def minimize_app(self) -> None:
        self.showMinimized()

    def exit_app(self) -> None:
        self.p.terminate()
        for thread in self.threads:
            thread.join()
        sys.exit(0)


def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()

    gui = RootWindow(model_name="facebook/wav2vec2-large-960h")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
