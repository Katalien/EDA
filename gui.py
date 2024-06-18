import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView, QMessageBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FeatureSelectionWindow(QWidget):
    def __init__(self, features):
        super().__init__()
        self.setWindowTitle('Feature Selection')

        self.features = features
        self.selected_features = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.feature_list = QListWidget()
        self.feature_list.setSelectionMode(QAbstractItemView.MultiSelection)
        for feature in self.features:
            item = QListWidgetItem(feature)
            item.setCheckState(Qt.Unchecked)
            self.feature_list.addItem(item)
        layout.addWidget(self.feature_list)

        self.generate_button = QPushButton('Сгенерировать')
        self.generate_button.clicked.connect(self.generate)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate(self):
        self.selected_features = [item.text() for item in self.feature_list.selectedItems()]
        if not self.selected_features:
            QMessageBox.warning(self, 'Ошибка', 'Выберите хотя бы одну фичу')
            return
        self.close()
        self.parent().run()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Data Analysis App')
        self.setGeometry(100, 100, 800, 600)

        self.features = {'Contrast': None, 'Brightness': None, 'Color': None}

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
        if path:
            self.images_path_edit.setText(path)

    def browse_labels(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Labels Directory')
        if path:
            self.labels_path_edit.setText(path)

    def browse_masks(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Masks Directory')
        if path:
            self.masks_path_edit.setText(path)

    def browse_prediction(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Prediction Directory')
        if path:
            self.prediction_path_edit.setText(path)

    def select_features(self):
        self.feature_window = FeatureSelectionWindow(list(self.features.keys()))
        self.feature_window.setParent(self, Qt.Dialog)
        self.feature_window.show()

    def generate(self):
        images_path = self.images_path_edit.text()
        if not images_path:
            QMessageBox.warning(self, 'Ошибка', 'Укажите путь к изображениям')
            return
        self.run()

    def run(self):
        # Здесь будет ваша логика генерации графиков на основе выбранных данных и фичей
        graphs = self.generate_graphs()

        self.show_graphs(graphs)

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

