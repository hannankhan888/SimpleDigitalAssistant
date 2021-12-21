import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QFrame, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from utils.dynamicPyQt5Labels import CustomButton


class RootWindow(QMainWindow):
    def __init__(self):
        super(RootWindow, self).__init__()

        self.WIDTH = 1024
        self.HEIGHT = 576
        self.app_name = "SimpleDigitalAssistant"

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
        self.font_family = self.font_database.applicationFontFamilies(self.lato_font_id).__getitem__(0)
        self.current_font = QFont(self.font_family, 20)

        self._init_colors()

        # create a main frame for overall layout
        self.main_frame = QFrame()
        self.main_frame_stylesheet = """
        QFrame {background-color: rgb(255, 232, 214)}
        """
        self.main_frame.setStyleSheet(self.main_frame_stylesheet)

        self.main_frame_layout = QVBoxLayout()
        self.main_frame_layout.setSpacing(0)
        self.main_frame_layout.setContentsMargins(0, 5, 0, 0)
        self.main_frame_layout.setAlignment(Qt.AlignTop)
        self.setWindowTitle(self.app_name)

        self.welcome_label = QLabel()
        self.welcome_label.setFont(self.current_font)
        self.welcome_label.setStyleSheet("""
        QLabel { rgb (88, 105, 126); }
        """)
        self.welcome_label.setText(
            "Welcome to your digital assistant,\nMAX!")

        self._init_window_frame()
        self.main_frame_layout.addWidget(self.welcome_label)
        self.main_frame.setLayout(self.main_frame_layout)

        self.setCentralWidget(self.main_frame)
        self.show()

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

    def _init_window_frame(self):
        self.window_frame = QtWidgets.QFrame()
        self.window_frame.setFixedHeight(40)
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
        self.wf_left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.wf_right_layout = QtWidgets.QHBoxLayout()
        self.wf_right_layout.setSpacing(0)
        self.wf_right_layout.setContentsMargins(0, 0, 0, 0)
        self.wf_right_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.app_name_label = CustomButton(self.about)
        self.app_name_label.setText(self.app_name)
        self.app_name_label.set_all_colors(self.normal_bg, self.highlight_bg, self.normal_color,
                                           self.highlight_color)
        self.wf_left_layout.addWidget(self.app_name_label)

        self.minimize_button_label = CustomButton(self.minimize_app)
        self.minimize_button_label.set_all_colors(self.normal_bg, self.highlight_bg, self.normal_color,
                                                  self.highlight_color)
        self.minimize_button_label.setText(" _ ")
        self.wf_right_layout.addWidget(self.minimize_button_label)

        self.close_button_label = CustomButton(self.exit_app)
        self.close_button_label.set_all_colors(self.normal_bg, self.highlight_bg, self.normal_color,
                                               self.highlight_color)
        self.close_button_label.setText(" / ")
        self.wf_right_layout.addWidget(self.close_button_label)

        self.window_frame_left.setLayout(self.wf_left_layout)
        self.window_frame_right.setLayout(self.wf_right_layout)

        self.window_frame_layout.addWidget(self.window_frame_left)
        self.window_frame_layout.addWidget(self.window_frame_right)

        self.window_frame.setLayout(self.window_frame_layout)

        self.main_frame_layout.addWidget(self.window_frame)

    def about(self):
        """This function takes care of the about dialog."""

        about_dialog = FramelessDialog(self, "Created by Hannan Khan, Salman Nazir,\nReza Mohideen, and Ali Abdul-Hameed.", self.normal_bg, self.highlight_bg,
                                       self.normal_color, self.highlight_color, "About", self.current_font)
        # if self.always_on_top:
        #     about_dialog.setWindowFlag(Qt.WindowStaysOnTopHint)

        github_label = QtWidgets.QLabel()
        github_label.setFont(self.current_font)
        github_label.setText('<a href="https://github.com/hannankhan888/SimpleDigitalAssistant" style="color: rgba(187, 172, 193, '
                             '255)">Github</a>')
        github_label.setOpenExternalLinks(True)

        # TODO: add a self.license_box() to display the license in the app.
        license_label = CustomButton()
        license_label.set_all_colors(self.normal_bg, self.highlight_bg, self.normal_color, self.highlight_color)
        license_label.setFont(self.current_font)
        license_label.setText("License")
        license_label.setCursor(Qt.PointingHandCursor)

        about_dialog.middle_frame_layout.addWidget(github_label)
        about_dialog.middle_frame_layout.addWidget(license_label)
        # self.main_frame_blur.setEnabled(True)
        result = about_dialog.exec_()
        # if result == 0:
        #     self.main_frame_blur.setEnabled(False)

    def minimize_app(self):
        self.showMinimized()

    def exit_app(self):
        sys.exit(0)


def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()
    gui = RootWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
