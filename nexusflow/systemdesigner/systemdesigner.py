import json
import logging
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QGroupBox, QDialog, QPlainTextEdit, \
    QComboBox, QVBoxLayout, QHBoxLayout

from nexusflow.settingsdialog import SettingsDialog
from nexusflow.systemdesigner.module.module import ModuleManager
from nexusflow.utils import str_to_datatype
from nexusflow.systemdesigner.module.predefinedwidgetmanager import register_predefined_gui_component
from nexusflow.systemdesigner.controllers.okfpga import OKFPGAController

logging.basicConfig(level=logging.DEBUG)

data = {
    'description': {
        "type": 'str',
        "display": True,
        "editable": True,
        "value": ""
    }
}


class EditSystemDialog(QDialog):
    def __init__(self, description: str):
        super().__init__()
        self.setWindowTitle("Edit system info")
        self.setModal(True)
        # self.setFixedSize(400, 300)

        self.description = description

        self.layout = QGridLayout()

        self.layout.addWidget(QLabel("Description"), 0, 0)
        self.description_line_edit = QPlainTextEdit()
        self.description_line_edit.setPlainText(self.description)
        self.description_line_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.layout.addWidget(self.description_line_edit, 0, 1)
        self.confirm_button = QPushButton('Confirm')
        self.confirm_button.clicked.connect(self.confirm_button_handler)
        self.layout.addWidget(self.confirm_button, 1, 1, 1, 2)
        self.setLayout(self.layout)

    def confirm_button_handler(self):
        self.description = self.description_line_edit.toPlainText()
        self.accept()


class System(QWidget):
    metadata = ("name", "description", "version", "last_modified")

    def __init__(self, name: str, version: str, path: Path, new: bool) -> None:
        """ System class for NexusFlow
        """
        # Properties
        # Metadata
        self.name = name
        self.path = path
        self.version = version
        self.controllers = {}

        if new:
            self.data = data
            with open(self.path / 'system.json', 'w') as file:
                json.dump(self.data, file)
            version_path = self.path / self.version
            version_path.mkdir(exist_ok=True)
        else:
            with open(self.path / 'system.json', 'r') as file:
                self.data = json.load(file)

        # GUI Bootstrap
        super().__init__()
        self.bold_font = QFont()
        self.bold_font.setBold(True)
        self.main_layout = QVBoxLayout()
        self.top_bar()
        self.module_manager = ModuleManager()
        self.main_layout.addWidget(self.module_manager)
        self.setLayout(self.main_layout)

        # DEVELOPMENT
        # self.module_manager.import_functions("C:/Users/aspus/Desktop/ADD_adapter_test.xlsm")
        # self.module_manager.import_functions("C:/Users/aspus/Desktop/PA 1 MM-N35-I49 R10mOhm.xlsm")
        # self.module_manager.import_functions("C:/Users/aspus/Desktop/NEVO+HDS1500 v1-interface11_nevo3.xlsm")

    def top_bar(self):
        top_bar_widget = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.system_info())
        top_bar_layout.addWidget(self.controller_group())
        top_bar_layout.insertStretch(2)
        top_bar_layout.addWidget(self.module_controls_group())
        top_bar_widget.setLayout(top_bar_layout)
        self.main_layout.addWidget(top_bar_widget)

    def system_info(self) -> QGroupBox:
        group = QGroupBox("System info")
        group_layout = QGridLayout()

        name_label = QLabel("Name:")
        name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(name_label, 0, 0)
        name = ''
        for word in self.name.split('-'):
            name += word.capitalize() + ' '
        name_value_label = QLabel(name)
        name_value_label.setFont(self.bold_font)
        group_layout.addWidget(name_value_label, 0, 1)
        version_label = QLabel("Version:")
        version_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(version_label, 1, 0)
        version_value_label = QLabel(self.version)
        version_value_label.setFont(self.bold_font)
        group_layout.addWidget(version_value_label, 1, 1)

        group.setLayout(group_layout)
        return group

    def controller_group(self) -> QGroupBox:
        group = QGroupBox("Hardware Controllers")
        group_layout = QGridLayout()
        controller_selection_combo = QComboBox()
        controller = OKFPGAController()
        self.controllers[controller.name] = controller
        register_predefined_gui_component(controller.name, self.controllers[controller.name])

        controller_selection_combo.addItem("Opal Kelly FPGA")
        group_layout.addWidget(controller_selection_combo, 0, 0)
        add_controller_button = QPushButton("Add")
        group_layout.addWidget(add_controller_button, 0, 1)
        controller_settings_button = QPushButton("Settings")
        group_layout.addWidget(controller_settings_button, 1, 1)
        group.setLayout(group_layout)
        return group

    def module_controls_group(self) -> QGroupBox:
        group = QGroupBox('Module')
        group_layout = QGridLayout()
        add_button = QPushButton("Add")
        add_button.setDisabled(True)
        # add_button.clicked.connect(self.import_module_button_handler)
        group_layout.addWidget(add_button, 0, 0)
        import_button = QPushButton("Import .xlsx")
        import_button.clicked.connect(self.import_module_button_handler)
        group_layout.addWidget(import_button, 1, 0)
        remove_button = QPushButton("Remove")
        # remove_button.clicked.connect(self.import_module_button_handler)
        group_layout.addWidget(remove_button, 2, 0)
        group.setLayout(group_layout)
        return group

    def load_from_file(self) -> None:
        """ Load a system from a path
        """
        with open(self.path / 'system.json', 'r') as file:
            self.data = json.loads(file.read())
        logging.info(f"Loading system {self.name}, version {self.version} from {self.path}")
        logging.debug(f"System data: {self.data}")

    def save_to_file(self) -> None:
        """ Save the system to a file
        """
        logging.debug(f"Saving system to {self.path}")
        with open(self.path / 'system.json', 'w') as f:
            f.write(json.dumps(self.data))

    def set_data_value(self, key: str, value: Any) -> None:
        """ Set a value in the system data

        :param key: The key to set
        :type key: str
        :param value: The value to set
        :type value: Any
        ...
        :raises TypeError: If the value is not of the correct type
        :raises KeyError: If the key is not found in the system data
        """
        if key in self.data.keys():
            if type(value) == str_to_datatype(self.data[key]['type']):
                self.data[key]['value'] = value
            else:
                raise TypeError(f"Value {value} is of type {type(value)}, expected: {self.data[key]['type']}")
        else:
            raise KeyError(f"Key {key} not found in system data")

    def get_data_value(self, key: str) -> Any:
        """ Get a value from the system data

        :param key: The key to get
        :type key: str
        ...
        :raises KeyError: If the key is not found in the system data
        ...
        :return: The value of the key
        :rtype: Any
        """
        if key in self.data.keys():
            return self.data[key]['value']
        else:
            raise KeyError(f"Key {key} not found in system data")

    def handle_edit_action(self) -> None:
        dialog = EditSystemDialog(self.data['description']['value'])
        if dialog.exec() == QDialog.Accepted:
            self.data['description']['value'] = dialog.description
            self.data_widgets['description'].setText(self.data['description']['value'])

    def import_module_button_handler(self):
        settings = {
            'Import from': {
                "type": 'path',
                "display": False,
                "editable": True,
                "value": "",
                "validator": "XLSX (*.xlsx)"
            }
        }
        dialog = SettingsDialog(settings)
        if dialog.exec() == QDialog.Accepted:
            self.module_manager.import_functions(dialog.settings['Import from']['value'])
