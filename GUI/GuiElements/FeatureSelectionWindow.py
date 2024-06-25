from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FeatureSelectionWindow(QWidget):
    def __init__(self, features, guiInfo):
        super().__init__()
        self.setWindowTitle('Feature Selection')

        self.features = features
        self.selected_features = []
        self.guiInfo = guiInfo

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.feature_list = QListWidget()
        self.feature_list.setSelectionMode(QAbstractItemView.NoSelection)
        for feature in self.features:
            item = QListWidgetItem(feature)
            item.setCheckState(Qt.Unchecked)
            self.feature_list.addItem(item)
        layout.addWidget(self.feature_list)

        self.generate_button = QPushButton('OK')
        self.generate_button.clicked.connect(self.confirm)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def confirm(self):
        self.selected_features = [item.text() for item in self.feature_list.findItems("*", Qt.MatchWildcard) if item.checkState() == Qt.Checked]
        self.guiInfo.set_features(self.selected_features)
        if not self.selected_features:
            QMessageBox.warning(self, 'Ошибка', 'Выберите хотя бы одну фичу')
            return
        self.close()
        # self.parent().update_features(self.selected_features)