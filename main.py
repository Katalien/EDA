from DatasetProcessor import EDAManager
from GUI.Gui import *
from GUI.GuiElements import MainWindow

if __name__ == "__main__":
    # manager = EDAManager.EDAManager("config2.yaml")
    # manager.run()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())








