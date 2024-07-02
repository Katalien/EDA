from DatasetProcessor import EDAManager
from GUI.Gui import *
from GUI.GuiElements import MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QVBoxLayout, QWidget, QGroupBox, QListWidget, \
    QListWidgetItem, QPushButton

class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("Main Window")
        self.main_window.setGeometry(100, 100, 600, 400)

        open_selection_window_button = QPushButton("Выбрать признаки и методы визуализации", self.main_window)
        open_selection_window_button.clicked.connect(self.open_feature_selection_window)
        self.main_window.setCentralWidget(open_selection_window_button)

        self.manager = EDAManager.EDAManager()

    def open_feature_selection_window(self):
        self.feature_selection_window = FeatureSelectionWindow(self)
        self.feature_selection_window.show()

    def process_selected_features(self, selected_features):
        print("Selected features and visualization methods:", selected_features)
        self.manager.run(selected_features)

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())