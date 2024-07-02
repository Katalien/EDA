from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton,
                             QGroupBox, QApplication, QMainWindow, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
import sys

class FeatureSelectionWindow(QWidget):
    selectionChanged = pyqtSignal(dict)  # Сигнал для передачи выбранных фичей

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.layout = QVBoxLayout(self)
        self.groups = []
        self.selected_features = {}  # Словарь для хранения выбранных признаков и методов
        self.option_dict = {
            "contrast": ["boxplot", "density", "scatter", "default"],
            "brightness": ["boxplot", "density", "scatter", "default"],
            "aspect ratio": ["boxplot", "default"],
            "classes frequency": ["default"],
        }

        for feature_name, visualizers in self.option_dict.items():
            group = self.create_feature_group(feature_name, visualizers)
            self.groups.append(group)
            self.layout.addLayout(group['layout'])

        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_selection)
        self.layout.addWidget(apply_button)

    def create_feature_group(self, feature_name, visualizers):
        feature_group = {}

        feature_layout = QVBoxLayout()

        checkbox = QCheckBox(feature_name)
        checkbox.setChecked(False)
        feature_layout.addWidget(checkbox)

        dropdown_button = QPushButton("Изменить выпадающий список")
        feature_layout.addWidget(dropdown_button)

        options_group = QGroupBox("Способы визуализации")
        options_group.setEnabled(False)
        options_layout = QVBoxLayout()

        option_checkboxes = []
        for vis_method in visualizers:
            option = QCheckBox(vis_method)
            options_layout.addWidget(option)
            option_checkboxes.append(option)

        options_group.setLayout(options_layout)
        options_group.setVisible(False)
        feature_layout.addWidget(options_group)

        feature_group['checkbox'] = checkbox
        feature_group['dropdown_button'] = dropdown_button
        feature_group['options_group'] = options_group
        feature_group['option_checkboxes'] = option_checkboxes
        feature_group['layout'] = feature_layout

        return feature_group

    def apply_selection(self):
        self.selected_features = {}
        for group in self.groups:
            feature_name = group['checkbox'].text()
            if group['checkbox'].isChecked():
                selected_methods = [cb.text() for cb in group['option_checkboxes'] if cb.isChecked()]
                self.selected_features[feature_name] = selected_methods
        self.selectionChanged.emit(self.selected_features)  # Отправляем сигнал с выбранными фичами

    def get_selected_features(self):
        return self.selected_features