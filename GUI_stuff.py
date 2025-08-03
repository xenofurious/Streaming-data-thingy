from qtpy import QtWidgets
from qtpy.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QDockWidget
from qtpy.QtCore import Qt
import sys
import os
import main as streaming_data

# some UI stuff setup?
os.environ["QT_API"] = "pyqt5"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My nuts hurt")
        self.setGeometry(100, 100, 300, 200)  # x, y, width, height

        self.label = QLabel("click me ~", self)
        self.button = QPushButton(self)
        self.button.clicked.connect(self.on_button_click)

        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()
        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)


        # set up sidebar
        self.sidebar = QDockWidget("display controls", self)
        self.sidebar.setMinimumWidth(150)
        self.sidebar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # sidebar content
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()


        self.sidebar.setWidget(sidebar_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.sidebar)



    def on_button_click(self):
        self.label.setText("Button Clicked!")


print(streaming_data.fetch_most_streamed_song_uri())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


