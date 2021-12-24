import sys
import threading

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QFrame, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from utils.dynamicPyQt5Labels import CustomButton, ScrollableLabel
from utils.dynamicPyQt5Labels import ImageChangingLabel, ImageBackgroundChangingLabel
from utils.framelessDialogs import FramelessMessageDialog, FramelessScrollableMessageDialog
import pyaudio
import numpy as np
import sounddevice as sd
from VoiceRecognition.Wav2vecLive.inference import Wave2Vec2Inference
from VoiceRecognition.Wav2vecLive.realTimeAudio import LiveWav2Vec2

CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 16000
NUMPY_DATATYPE = np.int16


class RootWindow(QMainWindow):
    def __init__(self, asr):
        super(RootWindow, self).__init__()

        self.asr = asr

        self.WIDTH = 1024
        self.HEIGHT = 576
        self.app_name = "SimpleDigitalAssistant"
        self.mousePressPos = None
        self.mouseMovePos = None
        self.recording = False
        self.p = None
        self.stream = None
        self.buffer = []
        self.np_buffer = None
        self.threads = []

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

        self._init_colors()
        self._init_sound_devices()

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

        self.bottom_main_frame = QFrame()
        self.bottom_main_frame_layout = QHBoxLayout()
        self.bottom_main_frame_layout.setSpacing(50)
        self.bottom_main_frame_layout.setContentsMargins(10, 70, 10, 10)
        self.bottom_main_frame_layout.setAlignment(Qt.AlignLeft)

        self.setWindowTitle(self.app_name)

        self.welcome_label = QLabel()
        self.welcome_label.setFont(self.current_font)
        self.welcome_label.setStyleSheet("""
        QLabel { rgb (88, 105, 126); }
        """)
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setText(
            "Welcome to your digital assistant, MAX!")

        self.output_label = ScrollableLabel("")
        self.output_label.setFont(QFont(self.lato_font_family, 10))
        self.output_label.message_label.setWordWrap(True)


        self.mic_label = ImageChangingLabel("resources/images/mic_normal_icon.png",
                                            "resources/images/mic_highlight_icon.png", self._start_recording_thread,
                                            350, 350)

        self._init_window_frame()
        self.bottom_main_frame_layout.addWidget(self.welcome_label)
        self.bottom_main_frame_layout.addWidget(self.output_label)
        self.bottom_main_frame_layout.addWidget(self.mic_label)
        self.bottom_main_frame.setLayout(self.bottom_main_frame_layout)
        self.main_frame_layout.addWidget(self.bottom_main_frame)
        self.main_frame.setLayout(self.main_frame_layout)

        self.setCentralWidget(self.main_frame)
        self.show()

    def _init_sound_devices(self):
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
        if (a0.button() == QtCore.Qt.LeftButton) and self.window_frame.underMouse():
            self.mousePressPos = a0.globalPos()
            self.mouseMovePos = a0.globalPos()
        super(RootWindow, self).mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if (a0.buttons() == QtCore.Qt.LeftButton) and (self.window_frame.underMouse()):
            curr_pos = self.pos()
            global_pos = a0.globalPos()
            diff = global_pos - self.mouseMovePos
            new_pos = curr_pos + diff
            self.move(new_pos)
            self.mouseMovePos = global_pos
        super(RootWindow, self).mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        super(RootWindow, self).mouseReleaseEvent(a0)

    def _init_colors(self):
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

    def _init_window_frame(self):
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

        self.minimize_button_label = CustomButton(self._start_asr, self.normal_bg,
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

    def start_asr_thread(self):
        self.asr_print_thread = threading.Thread(target=self._start_asr_printing)
        self.asr_print_thread.setDaemon(True)
        self.asr_print_thread.setName("Recording Thread")
        self.threads.append(self.asr_print_thread)
        self.asr_print_thread.start()

    def _start_asr_printing(self):
        try:
            while True:
                text, sample_length, inference_time = self.asr.get_last_text()
                print(f"{sample_length:.3f}s\t{inference_time:.3f}s\t{text}")

        except KeyboardInterrupt:
            self.asr.stop()

    def _start_asr(self):
        self.asr.start()
        self.start_asr_thread()

    def _start_recording_thread(self):
        self.recording_thread = threading.Thread(target=self.get_voice_command)
        self.recording_thread.setDaemon(True)
        self.recording_thread.setName("Recording Thread")
        self.threads.append(self.recording_thread)
        self.recording_thread.start()

    def get_voice_command(self):
        if self.recording:
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
            self._play_recorded_buffer_audio()
            return

        self.buffer = []
        self.stream = self.p.open(rate=SAMPLE_RATE, channels=CHANNELS, format=SAMPLE_FORMAT,
                                  frames_per_buffer=CHUNK, input=True)
        self.recording = True

        # data is of class 'bytes' and needs to converted into a numpy array.
        while self.recording:
            data = self.stream.read(1024)
            self.buffer.append(data)

    def _get_np_buffer(self):
        """Sets the numpy buffer by converting the bytes object into a numpy array.
        The numpy buffer can then be used for inference."""
        self.np_buffer = np.frombuffer(b''.join(self.buffer), dtype=NUMPY_DATATYPE)

    def _play_recorded_buffer_audio(self):
        self._get_np_buffer()
        print(self.np_buffer, "len:", len(self.np_buffer), "size in memory (bytes)",
              (self.np_buffer.size * self.np_buffer.itemsize))
        sd.play(self.np_buffer, SAMPLE_RATE)

    def about(self):
        """This function takes care of the about dialog."""

        about_dialog = FramelessMessageDialog(self,
                                              "Created by Hannan Khan, Salman Nazir,\nReza Mohideen, and Ali Abdul-Hameed.",
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

    def settings(self):
        pass

    def license(self):
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

    def minimize_app(self):
        self.showMinimized()

    def exit_app(self):
        self.p.terminate()
        for thread in self.threads:
            thread.join()
        sys.exit(0)


def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()

    asr = LiveWav2Vec2("facebook/wav2vec2-large-960h")

    gui = RootWindow(asr)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
