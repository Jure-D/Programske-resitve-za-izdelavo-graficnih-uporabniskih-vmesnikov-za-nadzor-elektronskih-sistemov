from typing import Optional, Any
from PySide6.QtWidgets import QWidget, QGridLayout, QGroupBox, QPushButton, QLabel, QLineEdit, QSpinBox, \
    QDoubleSpinBox, QCheckBox, QComboBox, QDialog, QApplication, QFileDialog, QDialogButtonBox
from PySide6.QtCore import Qt, Signal

from nexusflow.guidesigner.guicomponents.primitives.inputs import StringLineEdit, IntSpinBox, FloatSpinBox, \
    BoolCheckBox, ListComboBox, FileSelector


class SettingsDialog(QDialog):
    send_settings = Signal(dict)

    def __init__(self, settings: dict, name: Optional[str] = None):
        super().__init__()
        self.line_counter = 0
        self.setWindowTitle(f"{name} - Settings" if name else "Settings")
        self.setModal(True)
        self.layout = QGridLayout()

        self.settings = settings
        self.editing_widgets = {}

        for setting_key in settings.keys():
            if settings[setting_key]['editable']:
                setting_label = QLabel(setting_key.capitalize())
                setting_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.layout.addWidget(setting_label, self.line_counter, 0)

                if settings[setting_key]['type'] == 'str':
                    self.editing_widgets[setting_key] = StringLineEdit(settings[setting_key]['value'])
                    self.layout.addWidget(self.editing_widgets[setting_key], self.line_counter, 1)
                    self.line_counter += 1
                elif settings[setting_key]['type'] == 'int':
                    self.editing_widgets[setting_key] = IntSpinBox(
                        settings[setting_key].get('value', 0),
                        settings[setting_key].get('min_value', None),
                        settings[setting_key].get('max_value', None),
                        settings[setting_key].get('step', None)
                    )
                    self.layout.addWidget(self.editing_widgets[setting_key], self.line_counter, 1)
                    self.line_counter += 1
                elif settings[setting_key]['type'] == 'float':
                    self.editing_widgets[setting_key] = FloatSpinBox(
                        settings[setting_key].get('value', 0.0),
                        settings[setting_key].get('min_value', None),
                        settings[setting_key].get('max_value', None),
                        settings[setting_key].get('step', None)
                    )
                    self.layout.addWidget(self.editing_widgets[setting_key], self.line_counter, 1)
                    self.line_counter += 1
                elif settings[setting_key]['type'] == 'bool':
                    self.editing_widgets[setting_key] = BoolCheckBox(settings[setting_key]['value'])
                    self.layout.addWidget(self.editing_widgets[setting_key], self.line_counter, 1)
                    self.line_counter += 1
                elif settings[setting_key]['type'] == 'list':
                    self.editing_widgets[setting_key] = ListComboBox(
                        settings[setting_key]['value'],
                        settings[setting_key]['options']
                    )
                    self.layout.addWidget(self.editing_widgets[setting_key], self.line_counter, 1)
                    self.line_counter += 1
                elif settings[setting_key]['type'] == 'path':
                    self.editing_widgets[setting_key] = FileSelector(
                        settings[setting_key]['value'],
                        settings[setting_key]['validator']
                    )
                    self.layout.addWidget(self.editing_widgets[setting_key], self.line_counter, 1)
                    self.line_counter += 1
                else:
                    raise ValueError(f"Unknown setting type: {settings[setting_key]['type']}")

        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.dialog_buttons.accepted.connect(self.handle_accept)
        self.dialog_buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.dialog_buttons, self.line_counter, 0, 1, 2)

        self.setLayout(self.layout)

    def handle_accept(self) -> None:
        for setting_key in self.settings.keys():
            if self.settings[setting_key]['editable']:
                self.settings[setting_key]['value'] = self.editing_widgets[setting_key].get_value()
        self.send_settings.emit(self.settings)
        self.accept()


if __name__ == '__main__':
    example_settings = {
        'String setting': {
            "type": 'str',
            "display": True,
            "editable": True,
            "value": ""
        },
        'Int setting': {
            "type": 'int',
            "display": True,
            "editable": True,
            "value": 0,
            "min_value": 0,
            "max_value": 100,
            "step": 1,
        },
        'Float setting': {
            "type": 'float',
            "display": True,
            "editable": True,
            "value": 0.0,
            "min_value": 0.0,
            "max_value": 100.0,
            "step": 0.1
        },
        'Bool setting': {
            "type": 'bool',
            "display": True,
            "editable": True,
            "value": False
        },
        'Selector setting': {
            "type": 'list',
            "display": True,
            "editable": True,
            "value": 0,
            "options": ['Option 1', 'Option 2', 'Option 3']
        },
        'Path setting': {
            "type": 'path',
            "display": True,
            "editable": True,
            "value": "",
            "validator": "JSON (*.json)"
        }
    }

    app = QApplication()
    dialog = SettingsDialog(example_settings, "Example")
    dialog.show()
    app.exec()
