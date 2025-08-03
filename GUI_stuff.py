from qtpy import QtWidgets
from qtpy.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QFrame, QLabel, QPushButton, QWidget, QDockWidget, QSplitter
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
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        #central container widget
        container = QtWidgets.QWidget()
        self.setCentralWidget(container)

        main_layout = QtWidgets.QHBoxLayout()
        container.setLayout(main_layout)

        big_box_widget_stylesheet_thing = """
            QFrame {
                background-color: #444;
                padding: 4px;
                margin: 0px;
                }
        """


        #central widget frame
        central_frame = QtWidgets.QFrame()
        central_frame.setFrameShape(QtWidgets.QFrame.Box)
        central_frame.setStyleSheet(big_box_widget_stylesheet_thing)

        #central widget contents
        central_layout = QtWidgets.QVBoxLayout()
        central_layout.addWidget(QtWidgets.QLabel("central widget content"))
        central_frame.setLayout(central_layout)

        #sidebar widget frame
        sidebar_frame = QtWidgets.QFrame()
        sidebar_frame.setFrameShape(QtWidgets.QFrame.Box)
        sidebar_frame.setStyleSheet(big_box_widget_stylesheet_thing)
        sidebar_frame.setMinimumWidth(150)
        sidebar_frame.setMaximumWidth(250)

        #sidebar widget contents
        sidebar_layout = QtWidgets.QVBoxLayout()
        sidebar_layout.addWidget(QtWidgets.QLabel("sidebar widget content"))
        sidebar_frame.setLayout(sidebar_layout)

        #vertical qsplitter between the main window and the sidebar
        splitter = QtWidgets.QSplitter(Qt.Horizontal)
        splitter.addWidget(central_frame)
        splitter.addWidget(sidebar_frame)
        splitter.setStretchFactor(1,0)
        splitter.setStretchFactor(0, 1)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        #adding the widgets
        main_layout.addWidget(splitter)



print(streaming_data.fetch_most_streamed_song_uri())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


