from qtpy.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QWidget, QDockWidget, QSplitter
from qtpy.QtGui import QPixmap
from qtpy.QtCore import Qt
from io import BytesIO
import sys
import os

import main
import main as streaming_data
import requests

# some UI stuff setup?
os.environ["QT_API"] = "pyqt5"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My nuts hurt")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        #central container widget
        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout()
        container.setLayout(main_layout)

        big_box_widget_stylesheet_thing = """
            QFrame {
                background-color: #444;
                padding: 4px;
                margin: 0px;
                }
        """


        #central widget frame
        central_frame = QFrame()
        central_frame.setFrameShape(QFrame.Box)
        central_frame.setStyleSheet(big_box_widget_stylesheet_thing)

        #central widget contents
        central_layout = QVBoxLayout()
        image_url = main.fetch_image_from_track(main.fetch_most_streamed_song_uri(), 0)
        print(image_url)
        image_label = display_image(image_url)
        central_layout.addWidget(image_label)
        central_frame.setLayout(central_layout)

        #sidebar widget frame
        sidebar_frame = QFrame()
        sidebar_frame.setFrameShape(QFrame.Box)
        sidebar_frame.setStyleSheet(big_box_widget_stylesheet_thing)
        sidebar_frame.setMinimumWidth(150)
        sidebar_frame.setMaximumWidth(250)

        #sidebar widget contents
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QLabel("sidebar widget content"))
        sidebar_frame.setLayout(sidebar_layout)

        #vertical qsplitter between the main window and the sidebar
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(central_frame)
        splitter.addWidget(sidebar_frame)
        splitter.setStretchFactor(1,0)
        splitter.setStretchFactor(0, 1)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        #adding the widgets
        main_layout.addWidget(splitter)


#print(streaming_data.fetch_most_streamed_song_uri())


def display_image(image_url):
    response = requests.get(image_url)
    image_pixmap = QPixmap()
    image_pixmap.loadFromData(
        BytesIO(response.content).read())  # i have absolutely no idea what this does. learn later!

    my_label = QLabel()
    my_label.setPixmap(image_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
    return my_label

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


