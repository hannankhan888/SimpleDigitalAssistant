#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a minimalist frameless QDialog."""

__author__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__copyright__ = "Copyright 2022, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan", "Salman Nazir", "Reza Mohideen", "Ali Abdul-Hameed"]
__license__ = "MIT"

import os

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from dynamicPyQt5Labels import ColorChangingLabel, CustomButton, ScrollableLabel


def open_windows_sound_settings(event):
    # wont work if wrapped as @staticmethod
    os.system('cmd /c "start ms-settings:sound"')


class FramelessDialog(QtWidgets.QDialog):
    """This class creates a QDialog with the windowFlag FramelessWindowHint enabled.
    It implements a minimalist window frame. The ' '/' ' and the ' '_' ' in the window frame
    can be replaced with any type of label (especially custom image labels) to represent
    the close and minimize button better.
    This class will have its own QDialog name in the window frame. It will also display
    a message in the middle dialog. This dialog will open DEAD CENTER in the QMainWindow
    that calls it.
    This class comes with one button only, ' 'ok' '. Other buttons can be added after creation.
    This class can be dragged around via the window frame, similar to the QMainWindow."""

    def __init__(self, master: QMainWindow = None, message: str = "", normal_bg: QtGui.QColor = None,
                 highlight_bg: QtGui.QColor = None, normal_color: QtGui.QColor = None,
                 highlight_color: QtGui.QColor = None, close_button_highlight_bg: QtGui.QColor = None,
                 close_button_highlight_color: QtGui.QColor = None, window_title: str = "",
                 current_font: QtGui.QFont = None):
        super(FramelessDialog, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.master = master
        self.message = message
        self.normal_bg = normal_bg
        self.highlight_bg = highlight_bg
        self.normal_color = normal_color
        self.highlight_color = highlight_color
        self.close_button_highlight_bg = close_button_highlight_bg
        self.close_button_highlight_color = close_button_highlight_color
        self.window_title = window_title
        self.current_font = current_font
        self.mousePressPos = None
        self.mouseMovePos = None

        self.setStyleSheet(self.get_style_sheet(for_dialog=True))
        self.main_frame_layout = QtWidgets.QVBoxLayout()
        self.main_frame_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.main_frame_layout.setContentsMargins(0, 0, 0, 0)

        self._init_window_frame()
        self._init_middle_frame()
        self._init_bottom_frame()
        self.setLayout(self.main_frame_layout)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        top_left = self.master.window().frameGeometry().topLeft()
        parent_center = self.master.window().rect().center()
        self.move(top_left + parent_center - self.rect().center())
        super(FramelessDialog, self).showEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mousePressPos = None
        self.mouseMovePos = None
        if (a0.button() == QtCore.Qt.LeftButton) and self.window_frame.underMouse():
            self.mousePressPos = a0.globalPos()
            self.mouseMovePos = a0.globalPos()
        super(FramelessDialog, self).mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if (a0.buttons() == QtCore.Qt.LeftButton) and (self.window_frame.underMouse()):
            curr_pos = self.pos()
            global_pos = a0.globalPos()
            diff = global_pos - self.mouseMovePos
            new_pos = curr_pos + diff
            self.move(new_pos)
            self.mouseMovePos = global_pos
        super(FramelessDialog, self).mouseMoveEvent(a0)

    def _init_window_frame(self):
        self.window_frame = QtWidgets.QFrame()
        self.window_frame_layout = QtWidgets.QHBoxLayout()
        self.window_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.window_frame_left = QtWidgets.QFrame()
        self.wf_left_layout = QtWidgets.QHBoxLayout()
        self.wf_left_layout.setAlignment(Qt.AlignLeft)
        self.wf_left_layout.setContentsMargins(8, 2, 0, 0)

        self.window_title_label = ColorChangingLabel(self.normal_bg, self.highlight_bg,
                                                     self.normal_color, self.highlight_color, False)
        self.window_title_label.setFont(self.current_font)
        self.window_title_label.setText(self.window_title)

        self.wf_left_layout.addWidget(self.window_title_label)
        self.window_frame_left.setLayout(self.wf_left_layout)

        self.window_frame_right = QtWidgets.QFrame()
        self.wf_right_layout = QtWidgets.QHBoxLayout()
        self.wf_right_layout.setAlignment(Qt.AlignRight)
        self.wf_right_layout.setContentsMargins(0, 0, 0, 0)

        self.close_button_label = CustomButton(self.exit_window, self.normal_bg,
                                               self.close_button_highlight_bg, self.normal_color,
                                               self.close_button_highlight_color)
        self.close_button_label.setFont(self.current_font)
        self.close_button_label.setText("   /   ")
        self.wf_right_layout.addWidget(self.close_button_label)

        self.window_frame_right.setLayout(self.wf_right_layout)

        self.window_frame_layout.addWidget(self.window_frame_left)
        self.window_frame_layout.addWidget(self.window_frame_right)

        self.window_frame.setLayout(self.window_frame_layout)
        self.main_frame_layout.addWidget(self.window_frame)

    def _init_middle_frame(self):
        self.middle_frame = QtWidgets.QFrame()
        self.middle_frame_layout = QtWidgets.QVBoxLayout()
        self.middle_frame_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.middle_frame.setLayout(self.middle_frame_layout)
        self.main_frame_layout.addWidget(self.middle_frame)

    def _init_bottom_frame(self):
        self.bottom_frame = QtWidgets.QFrame()
        self.bottom_frame_layout = QtWidgets.QHBoxLayout()
        self.bottom_frame_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.ok_button_label = CustomButton(self.exit_window, self.normal_bg, self.highlight_bg,
                                            self.normal_color, self.highlight_color)
        self.ok_button_label.setFont(self.current_font)
        self.ok_button_label.setText("  ok  ")
        self.bottom_frame_layout.addWidget(self.ok_button_label)

        self.bottom_frame.setLayout(self.bottom_frame_layout)
        self.main_frame_layout.addWidget(self.bottom_frame)

    def set_all_colors(self, normal_bg, highlight_bg, normal_color, highlight_color):
        self.normal_bg = normal_bg
        self.highlight_bg = highlight_bg
        self.normal_color = normal_color
        self.highlight_color = highlight_color

    def get_style_sheet(self, for_frame: bool = False, for_dialog: bool = False) -> str:
        red = str(self.normal_bg.red())
        green = str(self.normal_bg.green())
        blue = str(self.normal_bg.blue())
        rgb_portion = "".join([red, ", ", green, ", ", blue])
        style_sheet = ""
        if for_frame:
            style_sheet = """
            QFrame{
            background-color: rgba(%s,255);
            }""" % rgb_portion
        if for_dialog:
            style_sheet = """
                        QDialog{
                        background-color: rgba(%s,255);
                        border: 1px solid white;
                        }""" % rgb_portion
        return style_sheet

    def exit_window(self):
        self.close()


class FramelessMessageDialog(FramelessDialog):
    """This class implements a Frameless Dialog and displays a message in the
    middle frame."""

    def __init__(self, master: QMainWindow = None, message: str = "", normal_bg: QtGui.QColor = None,
                 highlight_bg: QtGui.QColor = None, normal_color: QtGui.QColor = None,
                 highlight_color: QtGui.QColor = None, close_button_highlight_bg: QtGui.QColor = None,
                 close_button_highlight_color: QtGui.QColor = None, window_title: str = "",
                 current_font: QtGui.QFont = None):
        super(FramelessMessageDialog, self).__init__(master, message, normal_bg,
                                                     highlight_bg, normal_color, highlight_color,
                                                     close_button_highlight_bg, close_button_highlight_color,
                                                     window_title, current_font)
        self.message_label = ColorChangingLabel(self.normal_bg, self.highlight_bg, self.normal_color,
                                                self.highlight_color, False)
        self.message_label.setFont(self.current_font)
        self.message_label.setText(self.message)
        self.middle_frame_layout.addWidget(self.message_label)


class FramelessScrollableMessageDialog(FramelessDialog):
    """This class implements a FramelessDialog with a scrollable, non-stylized message
    in its middle frame."""

    def __init__(self, master: QMainWindow = None, message: str = "", normal_bg: QtGui.QColor = None,
                 highlight_bg: QtGui.QColor = None, normal_color: QtGui.QColor = None,
                 highlight_color: QtGui.QColor = None, close_button_highlight_bg: QtGui.QColor = None,
                 close_button_highlight_color: QtGui.QColor = None, window_title: str = "",
                 current_font: QtGui.QFont = None):
        super(FramelessScrollableMessageDialog, self).__init__(master, message, normal_bg,
                                                               highlight_bg, normal_color, highlight_color,
                                                               close_button_highlight_bg, close_button_highlight_color,
                                                               window_title, current_font)

        self.master = master
        self.message_label = ScrollableLabel(message)
        self.middle_frame_layout.addWidget(self.message_label)


class FramelessSettingsDialog(FramelessDialog):
    """This class implements a frameless dialog which displays input output audio
    settings. It also includes a link to open the sound settings, so as to change the
    input/output devices."""

    def __init__(self, master: QMainWindow = None, message: str = "", normal_bg: QtGui.QColor = None,
                 highlight_bg: QtGui.QColor = None, normal_color: QtGui.QColor = None,
                 highlight_color: QtGui.QColor = None, close_button_highlight_bg: QtGui.QColor = None,
                 close_button_highlight_color: QtGui.QColor = None, window_title: str = "",
                 current_font: QtGui.QFont = None, input_device_name: str = "",
                 output_device_name: str = ""):
        super(FramelessSettingsDialog, self).__init__(master, message, normal_bg,
                                                      highlight_bg, normal_color, highlight_color,
                                                      close_button_highlight_bg, close_button_highlight_color,
                                                      window_title, current_font)

        self.master = master
        self.message = message
        self.input_device_name = input_device_name
        self.output_device_name = output_device_name
        self._init_windows_sound_settings_label()
        self._init_io_devices_layout()

    def _init_windows_sound_settings_label(self):
        self.open_windows_sound_settings_label = QtWidgets.QLabel()
        self.open_windows_sound_settings_label.setText(
            '<a style="color: rgba(6, 69, 173, 255)">open sound settings</a>')
        self.open_windows_sound_settings_label.setCursor(Qt.PointingHandCursor)
        self.open_windows_sound_settings_label.mousePressEvent = open_windows_sound_settings
        self.middle_frame_layout.addWidget(self.open_windows_sound_settings_label)

    def _init_io_devices_layout(self):
        self.IO_devices_layout = QtWidgets.QVBoxLayout()
        self.input_layout = QtWidgets.QHBoxLayout()
        self.input_label = QtWidgets.QLabel("Input:")
        self.input_device_label = QtWidgets.QLabel(self.input_device_name)
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.input_device_label)

        self.output_layout = QtWidgets.QHBoxLayout()
        self.output_label = QtWidgets.QLabel("Output:")
        self.output_device_label = QtWidgets.QLabel(self.output_device_name)
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output_device_label)

        self.IO_devices_layout.addLayout(self.input_layout)
        self.IO_devices_layout.addLayout(self.output_layout)
        self.middle_frame_layout.addLayout(self.IO_devices_layout)
