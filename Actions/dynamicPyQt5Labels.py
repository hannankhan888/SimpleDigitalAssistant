#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains various objects used to implement minimalist UI."""

__author__ = "Hannan Khan"
__copyright__ = "Copyright 2021, SimpleDigitalAssistant"
__credits__ = ["Hannan Khan"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Hannan Khan"
__email__ = "hannankhan888@gmail.com"

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt


class ColorChangingLabel(QtWidgets.QLabel):
    """This is a class for creating labels that will change color, based on mouse location.

    If the mouse is hovering over, the label changes color to highlight_color and highlight_bg.
    Otherwise the label resorts to the colors normal_color and normal_bg.

    A few extra helper functions are also defined in this class, such as:
    get_rgb_string()
    get_style_sheet()
    set_all_colors() {for changing the colors of a label on the fly.}"""

    def __init__(self, normal_bg: QtGui.QColor = None, highlight_bg: QtGui.QColor = None,
                 normal_color: QtGui.QColor = None, highlight_color: QtGui.QColor = None, highlightable: bool = True):
        super(ColorChangingLabel, self).__init__()
        self.normal_bg = normal_bg
        self.highlight_bg = highlight_bg
        self.normal_color = normal_color
        self.highlight_color = highlight_color
        self.highlightable = highlightable
        self.setStyleSheet(self.get_style_sheet(False))

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.highlightable:
            self.setStyleSheet(self.get_style_sheet(True))
        super(ColorChangingLabel, self).enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if self.highlightable:
            self.setStyleSheet(self.get_style_sheet(False))
        super(ColorChangingLabel, self).leaveEvent(a0)

    @staticmethod
    def get_rgb(color: QtGui.QColor = None) -> str:
        red = str(color.red())
        green = str(color.green())
        blue = str(color.blue())
        rgb_str = "".join([red, ", ", green, ", ", blue])

        return rgb_str

    def get_style_sheet(self, highlighted: bool = False):
        """:returns the stylesheet for a label based on if it is highlighted or not."""

        if highlighted:
            style_sheet = """
            QLabel {
            color: rgba(%s, 255);
            background-color: rgba(%s, 255);
            }""" % (self.get_rgb(self.highlight_color), self.get_rgb(self.highlight_bg))
            return style_sheet
        elif not highlighted:
            style_sheet = """
            QLabel {
            color: rgba(%s, 255);
            background-color: rgba(%s, 255);
            }""" % (self.get_rgb(self.normal_color), self.get_rgb(self.normal_bg))
            return style_sheet


class ImageChangingLabel(QtWidgets.QLabel):
    """This is a class for implementing a QLabel object that displays images depending
    on mouse location. This class can also invoke a function {from another class}, on
    a mousePressEvent, if the function is specified at all.

    If the mouse if hovering over the label, then the label will display the ' 'highlighted' '
    image which is image_2.
    Otherwise, the ' 'normal' ' image is image_1.

    The images can be resized. The images parameters are the file paths to the images.

    A useful helper function to call is invert_active_state() which will turn the label into
    its highlighted version until called again. This is great for showing that a label has
    been clicked."""

    def __init__(self, image_1: str = "", image_2: str = "", func: callable = None,
                 resized_x: int = 128, resized_y: int = 128):
        super(ImageChangingLabel, self).__init__()
        self.leftButtonClicked = False
        self.active = False

        self.func = func
        self.image_1 = image_1
        self.image_2 = image_2
        self.resized_x = resized_x
        self.resized_y = resized_y
        self.img_1_pixmap = QtGui.QPixmap(self.image_1).scaled(self.resized_x, self.resized_y, Qt.KeepAspectRatio)
        self.img_2_pixmap = QtGui.QPixmap(self.image_2).scaled(self.resized_x, self.resized_y, Qt.KeepAspectRatio)
        self.setPixmap(self.img_1_pixmap)

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if not self.active:
            self.setPixmap(self.img_2_pixmap)
        super(ImageChangingLabel, self).enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if not self.active:
            self.setPixmap(self.img_1_pixmap)
        super(ImageChangingLabel, self).leaveEvent(a0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.leftButtonClicked = False
        if ev.button() == Qt.LeftButton:
            self.leftButtonClicked = True
        super(ImageChangingLabel, self).mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.func:
            if self.leftButtonClicked and (ev.button() == Qt.LeftButton):
                self.func()
        super(ImageChangingLabel, self).mouseReleaseEvent(ev)

    def update(self) -> None:
        if self.active:
            self.setPixmap(self.img_2_pixmap)
        else:
            self.setPixmap(self.img_1_pixmap)
        super(ImageChangingLabel, self).update()

    def invert_active_state(self):
        self.active = (not self.active)
        self.update()


class ImageBackgroundChangingLabel(ImageChangingLabel):
    def __init__(self, normal_bg: QtGui.QColor = None, highlight_bg: QtGui.QColor = None,
                 image_1: str = "", image_2: str = "", func: callable = None,
                 resized_x: int = 128, resized_y: int = 128):
        super(ImageBackgroundChangingLabel, self).__init__(image_1, image_2,
                                                           func, resized_x, resized_y)
        self.normal_bg = normal_bg
        self.highlight_bg = highlight_bg

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet(self.get_style_sheet(self.highlight_bg))
        super(ImageBackgroundChangingLabel, self).enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet(self.get_style_sheet(self.normal_bg))
        super(ImageBackgroundChangingLabel, self).leaveEvent(a0)

    @staticmethod
    def get_style_sheet(background_color: QtGui.QColor = None) -> str:
        red = str(background_color.red())
        green = str(background_color.green())
        blue = str(background_color.blue())
        rgb_str = "".join([red, ", ", green, ", ", blue])

        style_sheet = """
        QLabel { background-color: rgb(%s); }
        """ % rgb_str

        return style_sheet


class CustomButton(ColorChangingLabel):
    """This class inherits ColorChangingLabel. It also has a mousePressEvent, and can
    invoke a given class method (func) if it is given. This is great for implementing
    minimalist frameless windows in which the close button will be represented by an
    ' '/' ' and the minimize button by ' '_' '.
    This class will also change color, and needs to initialized with color when possible."""

    def __init__(self, func: callable = None, normal_bg: QtGui.QColor = None,
                 highlight_bg: QtGui.QColor = None, normal_color: QtGui.QColor = None,
                 highlight_color: QtGui.QColor = None, highlightable: bool = True):

        super(CustomButton, self).__init__(normal_bg, highlight_bg, normal_color,
                                           highlight_color, highlightable)
        self.leftButtonClicked = False
        self.func = func

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.leftButtonClicked = False
        if ev.button() == Qt.LeftButton:
            self.leftButtonClicked = True
        super(CustomButton, self).mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.func:
            if (ev.button() == Qt.LeftButton) and (self.leftButtonClicked is True):
                self.func()
        super(CustomButton, self).mouseReleaseEvent(ev)


class LabelButton(QtWidgets.QLabel):
    """This class inherits QtWidgets.QLabel. It also has a mousePressEvent, and can
    invoke a given class method (func) if it is given. This is great for implementing
    minimalist frameless windows in which the close button will be represented by an
    ' '/' ' and the minimize button by ' '_' '.
    """

    def __init__(self, func: callable = None):
        super().__init__()
        self.leftButtonClicked = False
        self.func = func

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.leftButtonClicked = False
        if ev.button() == Qt.LeftButton:
            self.leftButtonClicked = True
        super(QtWidgets.QLabel, self).mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.func:
            if (ev.button() == Qt.LeftButton) and (self.leftButtonClicked is True):
                self.func()
        super(QtWidgets.QLabel, self).mouseReleaseEvent(ev)
