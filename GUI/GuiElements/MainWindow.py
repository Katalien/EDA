import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ..GuiInfo import GuiInfo
from .FeatureSelectionWindow import FeatureSelectionWindow
from DatasetProcessor.EDAManager import EDAManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Data Analysis App')
        self.setGeometry(100, 100, 800, 600)

        self.features = {'Contrast': None, 'Brightness': None, 'Color': None}
        self.gui_info = GuiInfo()


        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.images_path_label = QLabel('Images Path:')
        self.images_path_edit = QLineEdit()
        self.images_path_button = QPushButton('Browse')
        self.images_path_button.clicked.connect(self.browse_images)

        layout.addWidget(self.images_path_label)
        layout.addWidget(self.images_path_edit)
        layout.addWidget(self.images_path_button)

        self.labels_path_label = QLabel('Labels Path:')
        self.labels_path_edit = QLineEdit()
        self.labels_path_button = QPushButton('Browse')
        self.labels_path_button.clicked.connect(self.browse_labels)

        layout.addWidget(self.labels_path_label)
        layout.addWidget(self.labels_path_edit)
        layout.addWidget(self.labels_path_button)

        self.masks_path_label = QLabel('Masks Path:')
        self.masks_path_edit = QLineEdit()
        self.masks_path_button = QPushButton('Browse')
        self.masks_path_button.clicked.connect(self.browse_masks)

        layout.addWidget(self.masks_path_label)
        layout.addWidget(self.masks_path_edit)
        layout.addWidget(self.masks_path_button)

        self.prediction_path_label = QLabel('Prediction Path:')
        self.prediction_path_edit = QLineEdit()
        self.prediction_path_button = QPushButton('Browse')
        self.prediction_path_button.clicked.connect(self.browse_prediction)

        layout.addWidget(self.prediction_path_label)
        layout.addWidget(self.prediction_path_edit)
        layout.addWidget(self.prediction_path_button)

        self.feature_button = QPushButton('Выбрать фичи')
        self.feature_button.clicked.connect(self.select_features)
        layout.addWidget(self.feature_button)

        self.generate_button = QPushButton('Сгенерировать')
        self.generate_button.clicked.connect(self.generate)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def browse_images(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Images Directory')
        self.gui_info.set_images_path(path)
        if path:
            self.images_path_edit.setText(path)

    def browse_labels(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Labels Directory')
        self.gui_info.set_labels_path(path)
        if path:
            self.labels_path_edit.setText(path)

    def browse_masks(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Masks Directory')
        self.gui_info.set_masks_path(path)
        if path:
            self.masks_path_edit.setText(path)

    def browse_prediction(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Prediction Directory')
        self.gui_info.set_predictions_path(path)
        if path:
            self.prediction_path_edit.setText(path)

    def select_features(self):
        self.feature_window = FeatureSelectionWindow(list(self.features.keys()), self.gui_info)
        self.feature_window.setParent(self, Qt.Dialog)
        self.feature_window.show()

    def generate(self):
        images_path = self.images_path_edit.text()
        if not images_path:
            QMessageBox.warning(self, 'Ошибка', 'Укажите путь к изображениям')
            return
        self.run()

    def run(self):
        print("run")
        manager = EDAManager(config_path="config2.yaml")
        manager.run()

    def generate_graphs(self):
        # Пример генерации графиков
        graphs = []
        for feature in self.feature_window.selected_features:
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 4, 9], label=feature)
            ax.legend()
            graphs.append(fig)
        return graphs

    def show_graphs(self, graphs):
        self.graph_window = QWidget()
        self.graph_window.setWindowTitle('Generated Graphs')
        layout = QVBoxLayout()
        for fig in graphs:
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
        self.graph_window.setLayout(layout)
        self.graph_window.show()