from qtpy.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QWidget, QDockWidget, QSplitter
from qtpy.QtGui import QPixmap
from qtpy.QtCore import Qt
from io import BytesIO
import sys
import os

import main as streaming_data
import requests

# some UI stuff setup?
os.environ["QT_API"] = "pyqt6"


#constants
padding = 10

#stylesheets - this really should be in its own script at some point.
big_box_widget_stylesheet_thing = f"""
            QFrame {{
                background-color: #444;
                padding: {padding}px;
                margin: 0px;
                }}
        """
small_box_widget_stylesheet_thing = f"""
    QFrame {{
        background-color: #333;
        padding: {padding}px;
        margin: 0px;
        }}
"""

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My nuts hurt")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        #central container widget
        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout()
        container.setLayout(main_layout)

        central_frame = CentralFrame()
        sidebar_frame = SidebarFrame()

        #vertical qsplitter between the main window and the sidebar
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(central_frame)
        splitter.addWidget(sidebar_frame)
        splitter.setStretchFactor(1,0)
        splitter.setStretchFactor(0, 1)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setHandleWidth(padding)

        #adding the widgets
        main_layout.addWidget(splitter)


class CentralFrame(QFrame):
    def __init__(self):
        super().__init__()

        # central frame
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet(big_box_widget_stylesheet_thing)

        # central frame contents
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignTop)
        central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(central_layout)

        #adding the subframe
        sub_central_frame = SubCentralFrame()
        central_layout.addWidget(sub_central_frame)

class SubCentralFrame(QFrame):
    def __init__(self):
        super().__init__()

        #central frame subframe
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet(small_box_widget_stylesheet_thing)
        self.setFixedHeight(100)


        #central frame subframe contents
        sub_central_layout = QHBoxLayout()
        sub_central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(sub_central_layout)


        image_url = streaming_data.fetch_image_from_track(streaming_data.fetch_most_streamed_song_uri(), 2)
        image_label = self.display_image(image_url, self.height()-2*padding)
        sub_central_layout.addWidget(image_label)

class SidebarFrame(QFrame):
    def __init__(self):
        super().__init__()

        #sidebar frame
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet(big_box_widget_stylesheet_thing)
        self.setMinimumWidth(150)
        self.setMaximumWidth(250)

        #sidebar frame contents
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addWidget(QLabel("sidebar widget content"))
        self.setLayout(sidebar_layout)

    def display_image(self, image_url, height):
        response = requests.get(image_url)
        image_pixmap = QPixmap()
        image_pixmap.loadFromData(
            BytesIO(response.content).read())  # i have absolutely no idea what this does. learn later!
        my_label = QLabel()
        my_label.setStyleSheet("padding: 0px; margin: 0px;")
        my_label.setPixmap(image_pixmap.scaled(height, height))

        return my_label

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())


