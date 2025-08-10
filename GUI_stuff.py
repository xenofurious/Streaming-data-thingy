from qtpy.QtWidgets import (QMainWindow, QApplication, QHBoxLayout,
                            QVBoxLayout, QFrame, QLabel, QScrollArea,
                            QWidget, QSplitter)
from qtpy.QtGui import QPixmap
from qtpy.QtCore import Qt
from io import BytesIO
from pathlib import Path
import sys
import os
import main as streaming_data
import requests

# some UI stuff setup?
os.environ["QT_API"] = "pyqt6"


# constants
padding = 10
song_no = 10


# other global variables
top_songs = streaming_data.fetch_top_songs(song_no)
top_uris = streaming_data.fetch_top_uris(song_no)
split_uris = streaming_data.split_uris(top_uris, 20)
top_songs_urls = streaming_data.convert_uri_to_url(streaming_data.fetch_top_uris(padding), 2)

test_visualisation_stylesheet = """
    QFrame{
        background-color: #FF0000
    }

"""

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My nuts hurt")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # central container widget
        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout()
        container.setLayout(main_layout)

        central_frame = CentralFrame()
        sidebar_frame = SidebarFrame()

        # scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_frame)

        # vertical qsplitter between the main window and the sidebar
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(scroll_area)
        splitter.addWidget(sidebar_frame)
        splitter.setStretchFactor(1,0)
        splitter.setStretchFactor(0, 1)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setHandleWidth(padding)

        # adding the widgets
        main_layout.addWidget(splitter)


class CentralFrame(QFrame):
    def __init__(self):
        super().__init__()

        # central frame
        self.setFrameShape(QFrame.Box)
        self.setObjectName("big_box_widget_stylesheet_thing")

        # central frame contents
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignTop)
        central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(central_layout)



        # adding the subframe
        for i in range(song_no):
            image_url = top_songs_urls.iloc[i]
            song_artist, song_title = top_songs.iloc[i]
            sub_central_frame = SubCentralFrame(image_url, song_artist, song_title)
            central_layout.addWidget(sub_central_frame)


# when i get multiple different songs working, i'll have to pass the image data as a parameter here!
class SubCentralFrame(QFrame):
    def __init__(self, image_url, song_artist, song_title):
        super().__init__()
        self.image_url = image_url
        self.song_artist = song_artist
        self.song_title = song_title


        # defining the frame
        self.setFrameShape(QFrame.Box)
        self.setObjectName("small_box_widget_stylesheet_thing")
        self.setFixedHeight(70)

        # defining the layout
        sub_central_layout = QHBoxLayout()
        sub_central_layout.setAlignment(Qt.AlignLeft)
        sub_central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(sub_central_layout)

        # contents!
        image_label = self.display_image(image_url, self.height()-2*padding)
        sub_central_layout.addWidget(image_label)

        # divider
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        sub_central_layout.addWidget(divider)

        # info!
        info_frame = InfoFrame(song_artist, song_title)
        sub_central_layout.addWidget(info_frame, stretch=1)




    def display_image(self, image_url, height):
        response = requests.get(image_url)
        image_pixmap = QPixmap()
        image_pixmap.loadFromData(
            BytesIO(response.content).read())  # i have absolutely no idea what this does. learn later!
        my_label = QLabel()
        my_label.setStyleSheet("padding: 0px; margin: 0px;")
        my_label.setPixmap(image_pixmap.scaled(height, height))
        return my_label

class InfoFrame(QFrame):
    def __init__(self, song_artist, song_title):
        super().__init__()
        self.song_artist = song_artist
        self.song_title = song_title

        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("padding: 0px; margin: 0px;")


        info_frame_layout = QVBoxLayout(self)
        info_frame_layout.setContentsMargins(0, 0, 0, 0)
        song_title_label = QLabel(song_title)
        song_artist_label = QLabel(song_artist)
        song_title_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        song_artist_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        info_frame_layout.addWidget(song_title_label)
        info_frame_layout.addWidget(song_artist_label)


class SidebarFrame(QFrame):
    def __init__(self):
        super().__init__()

        # sidebar frame
        self.setFrameShape(QFrame.Box)
        self.setObjectName("big_box_widget_stylesheet_thing")
        self.setMinimumWidth(150)
        self.setMaximumWidth(250)

        # sidebar frame contents
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addWidget(QLabel("sidebar widget content"))
        self.setLayout(sidebar_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("styles.qss").read_text().replace("PADDING", str(padding)))
    window = main_window()
    window.show()
    sys.exit(app.exec_())


