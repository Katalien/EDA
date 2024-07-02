from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QApplication
from PyQt5.QtCore import Qt
import sys
from GUI.GuiElements import MainWindow
from DatasetProcessor import DatasetManager

class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow.MainWindow(self)

        self.manager = DatasetManager.DatasetManager(self.main_window.output_area)

    def process_selected_features(self, selected_features):
        print("HAHA Selected features and visualization methods:", selected_features)
        # self.manager.run(selected_features)

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = Controller()
    controller.run()