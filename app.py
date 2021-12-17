import sys
from PyQt5.QtWidgets import *


class RootWindow(QMainWindow):
    def __init__(self):
        super(RootWindow, self).__init__()

        self.WIDTH = 1024
        self.HEIGHT = 576

        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)

        # opens the window in the middle of the screen.
        self.qtRectangle = self.frameGeometry()
        self.centerPoint = QDesktopWidget().availableGeometry().center()
        self.qtRectangle.moveCenter(self.centerPoint)
        self.move(self.qtRectangle.topLeft())


        #create a main frame for overall layout
        self.main_frame = QFrame()

        self.main_frame_layout = QHBoxLayout()

        self.setWindowTitle("SimpleDigitalAssistant")

        self.welcome_label = QLabel()
        self.welcome_label.setText("Welcome to your digital assistant, MAX!")

        self.main_frame_layout.addWidget(self.welcome_label)
        self.main_frame.setLayout(self.main_frame_layout)

        self.setCentralWidget(self.main_frame)
        self.show()


def main():
    app = QApplication(sys.argv)
    desktop = app.desktop()
    gui = RootWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
