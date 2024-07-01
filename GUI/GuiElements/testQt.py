from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QVBoxLayout, QWidget, QGroupBox, QListWidget, \
    QListWidgetItem, QPushButton


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.checkbox = QCheckBox("Enable options")
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.toggle_options)

        self.dropdown_button = QPushButton("Изменить выпадающий список")
        self.dropdown_button.clicked.connect(self.toggle_dropdown)

        self.options_group = QGroupBox("Options")
        self.options_group.setEnabled(False)

        self.options_layout = QVBoxLayout()

        self.option1 = QCheckBox("Option 1")
        self.option2 = QCheckBox("Option 2")
        self.option3 = QCheckBox("Option 3")

        self.options_layout.addWidget(self.option1)
        self.options_layout.addWidget(self.option2)
        self.options_layout.addWidget(self.option3)
        self.options_group.setLayout(self.options_layout)
        self.options_group.setVisible(False)

        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.dropdown_button)
        self.layout.addWidget(self.options_group)

    def toggle_options(self, state):
        self.options_group.setEnabled(state == Qt.Checked)

    def toggle_dropdown(self):
        self.options_group.setVisible(not self.options_group.isVisible())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CustomWidget()
    window.show()
    sys.exit(app.exec_())