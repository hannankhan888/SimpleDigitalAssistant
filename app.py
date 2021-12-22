import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QFrame, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from utils.dynamicPyQt5Labels import CustomButton, LabelButton
from utils.dynamicPyQt5Labels import ImageChangingLabel, ImageBackgroundChangingLabel
from utils.framelessDialog import FramelessDialog


class RootWindow(QMainWindow):
    def __init__(self):
        super(RootWindow, self).__init__()

        self.WIDTH = 1024
        self.HEIGHT = 576
        self.app_name = "SimpleDigitalAssistant"
        self.mousePressPos = None
        self.mouseMovePos = None

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

        self.mic_label = ImageChangingLabel("resources/images/mic_normal_icon.png",
                                            "resources/images/mic_highlight_icon.png", None,
                                            350, 350)

        self._init_window_frame()
        self.bottom_main_frame_layout.addWidget(self.welcome_label)
        self.bottom_main_frame_layout.addWidget(self.mic_label)
        self.bottom_main_frame.setLayout(self.bottom_main_frame_layout)
        self.main_frame_layout.addWidget(self.bottom_main_frame)
        self.main_frame.setLayout(self.main_frame_layout)

        self.setCentralWidget(self.main_frame)
        self.show()

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

    def about(self):
        """This function takes care of the about dialog."""

        about_dialog = FramelessDialog(self,
                                       "Created by Hannan Khan, Salman Nazir,\nReza Mohideen, and Ali Abdul-Hameed.",
                                       self.normal_bg, self.highlight_bg, self.normal_color,
                                       self.highlight_color, "About", self.current_font)

        github_label = QtWidgets.QLabel()
        github_label.setFont(self.current_font)
        github_label.setText(
            '<a href="https://github.com/hannankhan888/SimpleDigitalAssistant" style="color: rgba(187, 172, 193, '
            '255)">Github</a>')
        github_label.setOpenExternalLinks(True)

        # TODO: add a self.license_box() to display the license in the app.
        license_label = CustomButton(self.license, self.normal_bg, self.highlight_bg,
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
        pass

    def minimize_app(self):
        self.showMinimized()

    @staticmethod
    def exit_app():
        sys.exit(0)


def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()
    gui = RootWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
