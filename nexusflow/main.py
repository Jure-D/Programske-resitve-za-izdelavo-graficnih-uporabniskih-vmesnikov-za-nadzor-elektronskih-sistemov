from typing import Optional, List
import shutil
import sys
from pathlib import Path
import logging
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QDockWidget, QFileDialog, QDialog, QGridLayout, \
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QGroupBox, QDialogButtonBox, QSpacerItem, QSizePolicy, QCheckBox, \
    QButtonGroup, QRadioButton, QWidget, QComboBox
from PySide6.QtCore import Qt, Slot

from nexusflow.systemdesigner.systemdesigner import System
from guidesigner.guidesigner import GuiDesigner
from automationsdesigner.automationsdesigner import AutomationsDesigner
from nexusflow import router

logging.basicConfig(level=logging.DEBUG)


class WelcomeDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        logging.debug("Opening welcome dialog")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setModal(True)

        self.system_name: str = ''
        self.system_path: str = ''
        self.system_version: str = ''
        self.new: bool = False

        self.main_layout = QVBoxLayout()
        self.welcome_label = QLabel(
            "Welcome to NexusFlow!\n\n"
            "Here you can create a new project, open an existing one\nor create a new version of existing project.")
        self.main_layout.addWidget(self.welcome_label)

        self.new_system_radio_button = QRadioButton("New")
        self.new_system_radio_button.toggled.connect(self.radio_button_handler)
        self.main_layout.addWidget(self.new_system_radio_button)

        self.new_system_group = QGroupBox("Create new project")
        self.new_system_group.setEnabled(False)
        self.new_system_group_layout = QGridLayout()
        self.new_system_name_label = QLabel("Name:")
        self.new_system_name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.new_system_group_layout.addWidget(self.new_system_name_label, 0, 0)
        self.new_system_name_line_edit = QLineEdit()
        self.new_system_group_layout.addWidget(self.new_system_name_line_edit, 0, 1)

        self.new_system_version_label = QLabel("Version:")
        self.new_system_version_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.new_system_group_layout.addWidget(self.new_system_version_label, 1, 0)
        self.new_system_version_line_edit = QLineEdit()
        self.new_system_group_layout.addWidget(self.new_system_version_line_edit, 1, 1)

        self.new_system_location_label = QLabel("Location:")
        self.new_system_location_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.new_system_group_layout.addWidget(self.new_system_location_label, 2, 0)
        self.new_system_location_open_dialog_button = QPushButton('Browse')
        self.new_system_location_open_dialog_button.clicked.connect(self.new_system_path_button_handler)
        self.new_system_group_layout.addWidget(self.new_system_location_open_dialog_button, 2, 1)

        self.new_system_group.setLayout(self.new_system_group_layout)
        self.main_layout.addWidget(self.new_system_group)

        self.open_system_radio_button = QRadioButton("Open")
        self.open_system_radio_button.toggled.connect(self.radio_button_handler)
        self.main_layout.addWidget(self.open_system_radio_button)

        self.open_system_group = QGroupBox("Open existing project")
        self.open_system_group.setEnabled(False)
        self.open_system_group_layout = QGridLayout()
        self.open_system_location_label = QLabel("Location:")
        self.open_system_location_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.open_system_group_layout.addWidget(self.open_system_location_label, 0, 0)
        self.open_system_location_open_dialog_button = QPushButton('Browse')
        self.open_system_location_open_dialog_button.clicked.connect(self.open_system_button_handler)
        self.open_system_group_layout.addWidget(self.open_system_location_open_dialog_button, 0, 1)

        self.open_project_name_label = QLabel("Name:")
        self.open_project_name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.open_system_group_layout.addWidget(self.open_project_name_label, 1, 0)
        self.open_project_name_output_label = QLabel()
        self.open_system_group_layout.addWidget(self.open_project_name_output_label, 1, 1)

        self.open_system_version_label = QLabel("Version:")
        self.open_system_version_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.open_system_group_layout.addWidget(self.open_system_version_label, 2, 0)
        self.open_system_version_combo_box = QComboBox()
        self.open_system_version_combo_box.currentTextChanged.connect(self.system_version_combo_box_handler)
        self.open_system_group_layout.addWidget(self.open_system_version_combo_box, 2, 1)

        self.create_new_version_checkbox = QCheckBox("Create new version from that version")
        self.create_new_version_checkbox.stateChanged.connect(self.toggle_new_version)
        self.open_system_group_layout.addWidget(self.create_new_version_checkbox, 3, 0, 1, 2)
        self.new_version_label = QLabel("Version:")
        self.new_version_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.open_system_group_layout.addWidget(self.new_version_label, 4, 0)
        self.new_version_line_edit = QLineEdit()
        self.new_version_line_edit.setEnabled(False)
        self.open_system_group_layout.addWidget(self.new_version_line_edit, 4, 1)
        self.open_system_group.setLayout(self.open_system_group_layout)
        self.main_layout.addWidget(self.open_system_group)

        self.error_message = QLabel()
        self.error_message.setStyleSheet("color: red")
        self.main_layout.addWidget(self.error_message)

        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialog_buttons.accepted.connect(self.validate_data)
        self.dialog_buttons.rejected.connect(self.reject)
        self.main_layout.addWidget(self.dialog_buttons)
        self.setLayout(self.main_layout)

    def radio_button_handler(self):
        if self.new_system_radio_button.isChecked():
            self.new_system_group.setEnabled(True)
            self.open_system_group.setEnabled(False)
            self.new = True
        elif self.open_system_radio_button.isChecked():
            self.new_system_group.setEnabled(False)
            self.open_system_group.setEnabled(True)
            self.new = False
        else:
            self.new_system_group.setEnabled(False)
            self.open_system_group.setEnabled(False)

    def new_system_path_button_handler(self):
        self.system_path = Path(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def open_system_button_handler(self):
        self.system_path = Path(QFileDialog.getOpenFileName(self, "Select system file", filter='JSON (*.json)')[0]).parents[0]
        self.system_name = self.system_path.stem
        self.open_project_name_output_label.setText(self.system_name)
        for child_path in self.system_path.iterdir():
            if child_path.is_dir():
                self.open_system_version_combo_box.addItem(child_path.stem)

    def system_version_combo_box_handler(self):
        self.system_version = self.open_system_version_combo_box.currentText()
        logging.debug(f"Selected version: {self.system_version}")

    def toggle_new_version(self, state: int) -> None:
        if self.create_new_version_checkbox.isChecked():
            self.new_version_line_edit.setEnabled(True)
        else:
            self.new_version_line_edit.setEnabled(False)

    def validate_data(self):
        if self.new_system_radio_button.isChecked():
            if self.new_system_name_line_edit.text() == "":
                self.error_message.setText("Enter system name")
                return
            else:
                self.system_name = self.new_system_name_line_edit.text()

            if self.new_system_version_line_edit.text() == "":
                self.error_message.setText("Enter system version")
                return
            else:
                self.system_version = self.new_system_version_line_edit.text()

            if type(self.system_path) == str or self.system_path == Path():
                self.error_message.setText("Select system path")
                return

            self.system_path = self.system_path / self.new_system_name_line_edit.text()
            try:
                self.system_path.mkdir(parents=True, exist_ok=False)
            except FileExistsError:
                self.error_message.setText("System already exists")
                return

            logging.debug(f"Creating new system:\n"
                          f"name: {self.system_name}\n"
                          f"version: {self.system_version}\n"
                          f"location: {self.system_path}")
            self.accept()

        elif self.open_system_radio_button.isChecked():
            if self.system_path == "":
                self.error_message.setText("Select system.")
                return
            if self.create_new_version_checkbox.isChecked():
                if self.new_version_line_edit.text() == "":
                    self.error_message.setText("Enter new version.")
                    return

                new_version = self.new_version_line_edit.text()
                try:
                    new_version_path_path = self.system_path / new_version
                    new_version_path_path.mkdir(parents=True, exist_ok=False)
                    # Copy files from selected version to new version
                    source_path = self.system_path / self.system_version
                    for file in source_path.iterdir():
                        logging.debug(f"Copying {file} to {new_version_path_path}")
                        shutil.copy(file, new_version_path_path)
                    self.system_version = new_version
                except FileExistsError:
                    self.error_message.setText("Version already exists.")
            logging.debug(f"Opening system:\n"
                          f"name: {self.system_name}\n"
                          f"version: {self.system_version}\n"
                          f"location: {self.system_path}")
            self.accept()
        else:
            self.error_message.setText("Create or select a system.")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """ Main window of the application
        """
        super().__init__()

        # DEVELOPMENT
        # system_name = 'a-test-project'
        # system_version = 'v0'
        # system_path = Path('C:/Users/aspus/Desktop/nexusflow/a-test-project')
        # system_new = False
        # PRODUCTION
        welcome_dialog = WelcomeDialog()
        if welcome_dialog.exec() == QDialog.Accepted:
            logging.debug("Welcome dialog accepted")
            system_name = welcome_dialog.system_name
            system_version = welcome_dialog.system_version
            system_path = welcome_dialog.system_path
            system_new = welcome_dialog.new
        else:
            logging.debug("Welcome dialog denied")
            sys.exit()

        self.setWindowTitle("NexusFlow")
        # self.showMaximized()

        self.create_menu()

        self.statusBar().showMessage('Welcome to NexusFlow!')

        self.main_tabs_widget = QTabWidget()
        self.main_tabs = [
            "System Designer",
            "Automations Designer",
            "GUI Designer"
        ]

        self.system_designer = System(system_name, system_version, system_path, system_new)
        self.main_tabs_widget.addTab(self.system_designer, self.main_tabs[0])

        self.automations_designer = AutomationsDesigner()
        self.main_tabs_widget.addTab(self.automations_designer, self.main_tabs[1])

        self.gui_designer = GuiDesigner()
        self.gui_designer.statusbar_message.connect(self.statusBar().showMessage)
        self.main_tabs_widget.addTab(self.gui_designer, self.main_tabs[2])

        self.main_tabs_widget.currentChanged.connect(lambda index: self.setWindowTitle(f'NexusFlow - {self.main_tabs[index]}'))
        self.setCentralWidget(self.main_tabs_widget)

        # self.central_widget.currentChanged.connect(self.tab_changed_handler)

        self.system_runner_dock = QDockWidget("System Runner")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.system_runner_dock)
        self.system_runner_dock.hide()

    def create_menu(self) -> None:
        """ Creates menu bar
        """
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        save_project_action = file_menu.addAction("&Save")
        save_project_action.triggered.connect(self.save_action_handler)

        about_menu = self.menuBar().addMenu("&About")
        about_action = about_menu.addAction("&About")
        about_action.triggered.connect(self.about_action_handler)

    def save_action_handler(self) -> None:
        """ Handler for menu -> save system action
        """
        self.system_designer.save_to_file()

    def about_action_handler(self):
        pass


def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
