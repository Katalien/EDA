import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView, QMessageBox, QTextEdit, QCheckBox
from PyQt5.QtCore import Qt
from GUI.GuiElements.FeaturesSelectionWindow import FeatureSelectionWindow

class MainWindow(QMainWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Main Window")

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.setCentralWidget(self.output_area)

        self.dock_widget = QDockWidget("Feature Selection", self)
        self.feature_selection_window = FeatureSelectionWindow(self)
        self.dock_widget.setWidget(self.feature_selection_window)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)

        self.feature_selection_window.selectionChanged.connect(self.update_selected_features)

        self.showMaximized()

    def update_selected_features(self, selected_features):
        print("Selected features:", selected_features)
        self.controller.process_selected_features(selected_features)