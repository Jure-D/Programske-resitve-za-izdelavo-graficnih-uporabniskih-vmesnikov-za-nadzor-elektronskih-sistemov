import dataclasses
import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QFileDialog, QLCDNumber, QGroupBox, QPushButton, \
    QHBoxLayout, QDialog, QLineEdit, QDialogButtonBox, QLabel, QSpinBox, QTreeWidgetItem, QCheckBox, QComboBox, \
    QDoubleSpinBox, QFrame
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap
from dataclasses import dataclass
from typing import Optional, List, Tuple, Union

from nexusflow.guidesigner.guicomponents.primitives.outputs import Label
from nexusflow.utils import string_uuid
from nexusflow import router
from nexusflow.globalconstants import int_range, float_range
from nexusflow.utils import string_uuid
from nexusflow.systemdesigner.module.pindefinition import PinDefinition

logging.basicConfig(level=logging.DEBUG)


@dataclass(kw_only=True)
class GuiItemName:
    name: str = ''
    id: str = ''
    editable: bool = True


@dataclass(kw_only=True)
class GuiItemPositionData:
    column: Optional[int] = 0
    row: Optional[int] = 0
    editable: bool = True


@dataclass(kw_only=True)
class GuiContainerSettings:
    group: bool = False
    type: int = 0
    type_options: Tuple[str] = ('grid', 'vertical', 'horizontal')
    editable: bool = True


class GuiContainerItem(QTreeWidgetItem):
    def __init__(self):
        super().__init__(['', ''])
        self.name = GuiItemName(name="New Container")
        self.settings = GuiContainerSettings()
        self.position = GuiItemPositionData()
        self.generate_type_description()

    def generate_type_description(self):
        self.setText(0, self.name.name)
        self.setText(
            1,
            f'{"group_" if self.settings.group else ""}' +
            f'{self.settings.type_options[self.settings.type]}' +
            '_container' +
            f'@({self.position.column},{self.position.row})'
        )

    def show_settings_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle('Container Settings')
        dialog.setModal(True)
        dialog_layout = QVBoxLayout()

        name_group = QGroupBox('Name')
        name_group_layout = QVBoxLayout()
        name_lineedit = QLineEdit()
        name_lineedit.textChanged.connect(
            lambda text: setattr(self.name, 'name', text)
        )
        name_lineedit.setText(self.name.name)
        name_group_layout.addWidget(name_lineedit)
        name_group.setLayout(name_group_layout)
        name_group.setEnabled(self.name.editable)
        dialog_layout.addWidget(name_group)

        group_checkbox = QCheckBox('Group container')
        group_checkbox.stateChanged.connect(
            lambda state: setattr(self.settings, 'group', group_checkbox.isChecked())
        )
        group_checkbox.setChecked(self.settings.group)
        dialog_layout.addWidget(group_checkbox)

        container_type_group = QGroupBox('Container Type')
        container_type_group_layout = QVBoxLayout()
        container_type_combobox = QComboBox()
        container_type_combobox.currentIndexChanged.connect(
            lambda index: setattr(self.settings, 'type', index)
        )
        container_type_combobox.addItems(self.settings.type_options)
        container_type_combobox.setCurrentIndex(self.settings.type)
        container_type_group_layout.addWidget(container_type_combobox)
        container_type_group.setLayout(container_type_group_layout)
        container_type_group.setEnabled(self.settings.editable)
        dialog_layout.addWidget(container_type_group)

        position_group = QGroupBox('Position')
        position_group_layout = QGridLayout()
        position_group_layout.addWidget(QLabel('X:'), 0, 0)
        x_position_spinbox = QSpinBox()
        if self.position.column is not None:
            x_position_spinbox.setValue(self.position.column)
        x_position_spinbox.valueChanged.connect(
            lambda value: setattr(self.position, 'column', value)
        )
        x_position_spinbox.setRange(0, int_range[1])
        position_group_layout.addWidget(x_position_spinbox, 0, 1)
        position_group_layout.addWidget(QLabel('Y:'), 1, 0)
        y_position_spinbox = QSpinBox()
        if self.position.row is not None:
            y_position_spinbox.setValue(self.position.row)
        y_position_spinbox.valueChanged.connect(
            lambda value: setattr(self.position, 'row', value)
        )
        y_position_spinbox.setRange(0, int_range[1])
        position_group_layout.addWidget(y_position_spinbox, 1, 1)
        position_group.setLayout(position_group_layout)
        position_group.setEnabled(self.position.editable)
        dialog_layout.addWidget(position_group)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)

        if dialog.exec() == QDialog.Accepted:
            self.generate_type_description()

    def get_gui(self) -> QWidget | QGroupBox:
        if self.settings.group:
            container_widget = QGroupBox()
        else:
            container_widget = QWidget()
            container_widget.setWindowTitle(self.name.name)

        if self.settings.type == 0:
            container_layout = QGridLayout()
        elif self.settings.type == 1:
            container_layout = QVBoxLayout()
        elif self.settings.type == 2:
            container_layout = QHBoxLayout()
        else:
            raise ValueError(f'Unknown container type index: {self.settings.type}')

        container_widget.setWindowTitle(self.name.name)
        for child_index in range(self.childCount()):
            child = self.child(child_index)
            if self.settings.type == 0:
                new_entry = child.get_gui()
                if child.is_important:
                    container_layout.addWidget(new_entry, child.data.important_gui.row, child.important_gui.column, child.layout().rowCount(), child.layout().rowCount())
                else:
                    container_layout.addWidget(new_entry, child.data.main_gui.row, child.data.main_gui.column)
            else:
                container_layout.addWidget(child.get_gui())
        container_widget.setLayout(container_layout)

        return container_widget


@dataclass(kw_only=True)
class GuiIntInputSettings:
    initial: int = 0
    min: int = 0
    max: int = 100
    editable: bool = True


@dataclass(kw_only=True)
class GuiFloatInputSettings:
    initial: float = 0.0
    min: float = 0.0
    max: float = 1.0
    editable: bool = True


@dataclass(kw_only=True)
class GuiStringInputSettings:
    initial: str = ""
    editable: bool = True


@dataclass(kw_only=True)
class GuiBoolInputSettings:
    initial: bool = False
    editable: bool = True


@dataclass(kw_only=True)
class GuiListInputSettings:
    initial: int = 0
    options: List[str] = dataclasses.field(default_factory=list)
    editable: bool = True


@dataclass(kw_only=True)
class GuiPathInputSettings:
    initial: str = ""
    validator: str = "JSON (*.json)"
    editable: bool = True


InputValueSettings = Union[
    GuiIntInputSettings,
    GuiFloatInputSettings,
    GuiStringInputSettings,
    GuiBoolInputSettings,
    GuiListInputSettings,
    GuiPathInputSettings
]


@dataclass(kw_only=True)
class GuiInputSettings:
    type: int = 0
    type_options: Tuple[str] = ('int', 'float', 'bool', 'str', 'list', 'path')
    editable: bool = True
    value: InputValueSettings = None

    def init_value_settings(self):
        if self.get_selected_type() == 'str':
            self.value = GuiStringInputSettings()
        elif self.get_selected_type() == 'int':
            self.value = GuiIntInputSettings()
        elif self.get_selected_type() == 'float':
            self.value = GuiFloatInputSettings()
        elif self.get_selected_type() == 'bool':
            self.value = GuiBoolInputSettings()
        elif self.get_selected_type() == 'list':
            self.value = GuiListInputSettings()
        elif self.get_selected_type() == 'path':
            self.value = GuiPathInputSettings()
        else:
            raise ValueError(f'Unknown widget type: {self.get_selected_type()}')

    def get_selected_type(self) -> str:
        return self.type_options[self.type]


class GuiInputWidgetItem(QTreeWidgetItem):
    def __init__(self):
        super().__init__([f'New Input', ''])

    def add_data(self, data: PinDefinition, is_important: bool):
        self.data = data
        self.is_important = is_important
        # self.generate_type_description()

    def generate_type_description(self):
        self.setText(0, self.data.id)
        type_description = f'{self.data.main_gui.display_type}_input' \
                           f'@({self.data.important_gui.column if self.is_important else self.data.main_gui.column},' \
                           f'{self.data.important_gui.row if self.is_important else self.data.main_gui.row})'
        self.setText(
            1,
            type_description
        )

    def show_settings_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle('Input Settings')
        dialog.setModal(True)
        dialog_layout = QGridLayout()

        dialog_layout.addWidget(QLabel('Input Type:'), 0, 0)
        input_type_combobox = QComboBox()
        input_type_combobox.addItems(['str', 'int', 'bool', 'float', 'list', 'path'])
        input_type_combobox.setCurrentText(self.data.main_gui.display_type)
        input_type_combobox.currentTextChanged.connect(
            lambda text: update_input_type(text)
        )
        dialog_layout.addWidget(input_type_combobox, 0, 1)

        def update_input_type(display_type: str):
            self.data.main_gui.display_type = display_type
            draw_value_settings()

        value_group = QGroupBox('')

        def draw_value_settings():
            nonlocal value_group
            value_group.deleteLater()
            value_group = QGroupBox('Value settings')
            value_group_layout = QGridLayout()
            value_group_layout.addWidget(QLabel('Initial value:'), 0, 0)
            if self.data.main_gui.display_type == 'int' or self.data.main_gui.display_type == 'float':
                value_group_layout.addWidget(QLabel('Min. value:'), 1, 0)
                value_group_layout.addWidget(QLabel('Max. value:'), 2, 0)
                value_group_layout.addWidget(QLabel('Step:'), 3, 0)
                if self.data.main_gui.display_type == 'int':
                    initial_value_spinbox = QSpinBox()
                    initial_value_spinbox.setRange(int_range[0], int_range[1])

                    min_value_spinbox = QSpinBox()
                    min_value_spinbox.setRange(int_range[0], int_range[1])

                    max_value_spinbox = QSpinBox()
                    max_value_spinbox.setRange(int_range[0], int_range[1])

                    step_spinbox = QSpinBox()
                    step_spinbox.setRange(0, int_range[1])
                else:
                    initial_value_spinbox = QDoubleSpinBox()
                    initial_value_spinbox.setRange(float_range[0], float_range[1])

                    min_value_spinbox = QDoubleSpinBox()
                    min_value_spinbox.setRange(float_range[0], float_range[1])

                    max_value_spinbox = QDoubleSpinBox()
                    max_value_spinbox.setRange(float_range[0], float_range[1])

                initial_value_spinbox.setValue(self.data.value.initial)
                initial_value_spinbox.valueChanged.connect(
                    lambda value: setattr(self.data.value, 'initial', value)
                )
                value_group_layout.addWidget(initial_value_spinbox, 0, 1)

                min_value_spinbox.setValue(self.data.value.min)
                min_value_spinbox.valueChanged.connect(
                    lambda value: setattr(self.data.value, 'min', value)
                )
                value_group_layout.addWidget(min_value_spinbox, 1, 1)
                max_value_spinbox.setRange(int_range[0], int_range[1])
                max_value_spinbox.setValue(self.data.value.max)
                max_value_spinbox.valueChanged.connect(
                    lambda value: setattr(self.data.value, 'max', value)
                )
                value_group_layout.addWidget(max_value_spinbox, 2, 1)

            elif self.data.main_gui.display_type == 'bool':
                initial_value_checkbox = QCheckBox()
                initial_value_checkbox.setChecked(self.data.value.initial == 1)
                initial_value_checkbox.stateChanged.connect(
                    lambda state: setattr(self.data.value, 'initial', initial_value_checkbox.isChecked())
                )
                value_group_layout.addWidget(initial_value_checkbox, 0, 1)
            elif self.data.main_gui.display_type == 'str':
                initial_value_lineedit = QLineEdit()
                initial_value_lineedit.setText(self.data.value.initial)
                initial_value_lineedit.textChanged.connect(
                    lambda text: setattr(self.data.value, 'initial', text)
                )
                value_group_layout.addWidget(initial_value_lineedit, 0, 1)
            # elif self.data.main_gui.display_type == 'list':
            #     initial_value_combobox = QComboBox()
            #
            #     def update_combobox_items():
            #         initial_value_combobox.clear()
            #         initial_value_combobox.addItems(self.settings.value.options)
            #         initial_value_combobox.setCurrentIndex(self.settings.value.initial)
            #
            #     update_combobox_items()
            #     initial_value_combobox.setCurrentIndex(self.settings.value.initial)
            #     initial_value_combobox.currentIndexChanged.connect(
            #         lambda index: setattr(self.settings.value, 'initial', index)
            #     )
            #     value_group_layout.addWidget(initial_value_combobox, 0, 1)
            #
            #     value_group_layout.addWidget(QLabel('Add option:'), 1, 0)
            #     add_option_lineedit = QLineEdit()
            #     value_group_layout.addWidget(add_option_lineedit, 1, 1)
            #     add_option_button = QPushButton('Add')
            #
            #     def add_option():
            #         self.settings.value.options.append(add_option_lineedit.text())
            #         add_option_lineedit.setText('')
            #         update_combobox_items()
            #
            #     add_option_button.clicked.connect(add_option)
            #     value_group_layout.addWidget(add_option_button, 2, 0)
            #
            #     def remove_option():
            #         self.settings.value.options.pop(initial_value_combobox.currentIndex())
            #         update_combobox_items()
            #
            #     remove_option_button = QPushButton('Remove')
            #     remove_option_button.clicked.connect(remove_option)
            #     value_group_layout.addWidget(remove_option_button, 2, 1)

            # elif self.data.main_gui.display_type == 'path':
            #     initial_value_button = QPushButton('Select path')
            #     initial_value_button.clicked.connect(
            #         lambda: setattr(self.data.value, 'initial', QFileDialog.getExistingDirectory())
            #     )
            #     validator_lineedit = QLineEdit()
            #     validator_lineedit.setText(self.settings.validator)
            #     validator_lineedit.textChanged.connect(
            #         lambda text: setattr(self.settings, 'validator', text)
            #     )
            #     value_group_layout.addWidget(validator_lineedit, 1, 1)

            value_group.setLayout(value_group_layout)
            dialog_layout.addWidget(value_group, 1, 0, 1, 2)

        draw_value_settings()

        position_group = QGroupBox('Position')
        position_group_layout = QGridLayout()
        position_group_layout.addWidget(QLabel('X:'), 0, 0)
        x_position_spinbox = QSpinBox()
        if self.is_important:
            x_position_spinbox.setValue(self.data.important_gui.column)
            x_position_spinbox.valueChanged.connect(
                lambda value: setattr(self.data.important_gui, 'column', value)
            )
        else:
            x_position_spinbox.setValue(self.data.main_gui.column)
            x_position_spinbox.valueChanged.connect(
                lambda value: setattr(self.data.main_gui, 'column', value)
            )
        x_position_spinbox.setRange(0, int_range[1])
        position_group_layout.addWidget(x_position_spinbox, 0, 1)
        position_group_layout.addWidget(QLabel('Y:'), 1, 0)
        y_position_spinbox = QSpinBox()
        if self.is_important:
            y_position_spinbox.setValue(self.data.important_gui.row)
            y_position_spinbox.valueChanged.connect(
                lambda value: setattr(self.data.important_gui, 'row', value)
            )
        else:
            y_position_spinbox.setValue(self.data.main_gui.row)
            y_position_spinbox.valueChanged.connect(
                lambda value: setattr(self.data.main_gui, 'row', value)
            )
        y_position_spinbox.setRange(0, int_range[1])
        position_group_layout.addWidget(y_position_spinbox, 1, 1)
        position_group.setLayout(position_group_layout)
        dialog_layout.addWidget(position_group, 2, 0, 1, 2)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        dialog_layout.addWidget(button_box, 3, 0, 1, 2)
        dialog.setLayout(dialog_layout)

        if dialog.exec() == QDialog.Accepted:
            self.generate_type_description()

    def get_gui(self) -> QWidget:
        if self.data.main_gui.display_type == 'float' or self.data.main_gui.display_type == 'int':
            widget = QWidget()
            layout = QGridLayout()
            label = QLabel(self.data.name)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(label, 0, 0)
            step_editor = QComboBox()
            if self.data.main_gui.display_type == 'int':
                editor = QSpinBox()
                step_editor.addItems(['100', '10', '1'])
            else:
                editor = QDoubleSpinBox()
                step_editor.addItems(['100', '10', '1', '0.1', '0.01'])
            editor.setRange(self.data.value.min, self.data.value.max)
            editor.setValue(self.data.value.initial)
            # editor.setSingleStep(self.settings.value.step)
            layout.addWidget(editor, 0, 1)
            layout.addWidget(QLabel('Step:'), 1, 0)
            step_editor.setCurrentIndex(2)
            step_editor.currentIndexChanged.connect(
                lambda index: editor.setSingleStep(float(step_editor.currentText()))
            )
            layout.addWidget(step_editor, 1, 1)
            widget.setLayout(layout)

            # widget = QDoubleSpinBox()
            # widget.setRange(self.settings.value.min, self.settings.value.max)
            # widget.setValue(self.settings.value.initial)
            # widget.setSingleStep(self.settings.value.step)
            # widget.valueChanged.connect()
        elif self.data.main_gui.display_type == 'str':
            widget = QLineEdit()
            widget.setText(self.data.value.initial)
            # widget.textChanged.connect()
        # elif self.data.main_gui.display_type == 'list':
        #     widget = QComboBox()
        #     widget.addItems(self.data.value.options)
        #     widget.setCurrentIndex(self.data.value.initial)
            # widget.currentIndexChanged.connect()
        elif self.data.main_gui.display_type == 'path':
            widget = QPushButton('Browse')
            # widget.clicked.connect()
        elif self.data.main_gui.display_type == 'bool':
            widget = QWidget()
            layout = QGridLayout()
            layout.addWidget(QLabel(self.data.name), 0, 0)
            editor = QCheckBox()
            editor.setChecked(self.data.value.initial == 1)
            editor.stateChanged.connect(
                lambda state: router.route('aihfdoaousadpgfpef', {'function': 'ADD3 3', 'value': state == 2})
            )
            layout.addWidget(editor, 0, 1)
            widget.setLayout(layout)

            # widget = QCheckBox()
            # widget.setChecked(self.settings.value.initial)
            # widget.stateChanged.connect()

        # container_layout.addWidget(widget, self.position.row, self.position.column)
        return widget


@dataclass(kw_only=True)
class GuiIntOutputSettings:
    value: int = 0
    editable: bool = True


@dataclass(kw_only=True)
class GuiFloatOutputSettings:
    value: float = 0.0
    editable: bool = True


@dataclass(kw_only=True)
class GuiStringOutputSettings:
    value: str = ""
    editable: bool = True


@dataclass(kw_only=True)
class GuiBoolOutputSettings:
    value: bool = False
    editable: bool = True


@dataclass(kw_only=True)
class GuiListOutputSettings:
    value: int = 0
    options: List[str] = dataclasses.field(default_factory=list)
    editable: bool = True


@dataclass(kw_only=True)
class GuiPathOutputSettings:
    value: str = ""
    validator: str = "JSON (*.json)"
    editable: bool = True


OutputValue = Union[
    GuiIntOutputSettings,
    GuiFloatOutputSettings,
    GuiStringOutputSettings,
    GuiBoolOutputSettings,
    GuiListOutputSettings,
    GuiPathOutputSettings
]


@dataclass(kw_only=True)
class GuiOutputSettings:
    type: int = 0
    type_options: Tuple[str] = ('int', 'float', 'bool', 'str', 'list', 'path')
    editable: bool = True
    value: OutputValue = None

    def init_value_settings(self):
        if self.get_selected_type() == 'str':
            self.value = GuiStringOutputSettings()
        elif self.get_selected_type() == 'int':
            self.value = GuiIntOutputSettings()
        elif self.get_selected_type() == 'float':
            self.value = GuiFloatOutputSettings()
        elif self.get_selected_type() == 'bool':
            self.value = GuiBoolOutputSettings()
        elif self.get_selected_type() == 'list':
            self.value = GuiListOutputSettings()
        elif self.get_selected_type() == 'path':
            self.value = GuiPathOutputSettings()
        else:
            raise ValueError(f'Unknown widget type: {self.get_selected_type()}')

    def get_selected_type(self) -> str:
        return self.type_options[self.type]


class GuiOutputWidgetItem(QTreeWidgetItem):
    def __init__(self):
        super().__init__([f'New Output', ''])

    def add_data(self, data: PinDefinition, is_important: bool):
        self.data = data
        self.is_important = is_important
        # self.generate_type_description()

    def generate_type_description(self):
        self.setText(0, self.data.id)
        type_description = f'{self.data.main_gui.display_type}_output' \
                           f'@({self.data.important_gui.column if self.is_important else self.data.main_gui.column},' \
                           f'{self.data.important_gui.row if self.is_important else self.data.main_gui.row})'
        self.setText(
            1,
            type_description
        )

    def show_settings_handler(self):
        raise NotImplementedError

    def get_gui(self):
        label = QLabel(self.data.name)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        if self.data.main_gui.display_type == 'int' or self.data.main_gui.display_type == 'float':
            widget = QWidget()
            layout = QGridLayout()
            layout.addWidget(QLabel(self.data.name), 0, 0)
            editor = QLCDNumber()
            editor.setMode(QLCDNumber.Dec)
            editor.setSegmentStyle(QLCDNumber.Flat)
            # editor.setFrameStyle(QLCDNumber.NoFrame)
            editor.display(self.data.value.initial)
            layout.addWidget(editor, 0, 1)
            widget.setLayout(layout)
        elif self.data.main_gui.display_type == 'str':
            widget = QLabel(self.data.value.initial)
        elif self.data.main_gui.display_type == 'list':
            raise NotImplementedError
        elif self.data.main_gui.display_type == 'path':
            raise NotImplementedError
        elif self.data.main_gui.display_type == 'bool':
            widget = QWidget()
            layout = QGridLayout()
            layout.addWidget(QLabel(self.data.name), 0, 0)
            editor = QLabel()
            if self.data.value.initial == 1:
                editor.setStyleSheet(
                    'background-color: red;border: 2px solid black;border-radius: 7px;max-width: 14px;max-height: 14px;')
            else:
                editor.setStyleSheet(
                    'background-color: gray;border: 2px solid black;border-radius: 7px;max-width: 14px;max-height: 14px;')
            layout.addWidget(editor, 0, 1)

        return widget


class GuiControllerWidgetItem(QTreeWidgetItem):
    def __init__(self):
        super().__init__([f'OpalKelly FPGA', 'fpga_controller'])
        self.uuid = string_uuid()
        self.position = GuiItemPositionData()
        router.register_route('asdoncdsajcbds', self.route_handler)

    def route_handler(self, payload):
        if payload['function'] == 'on':
            self.is_connected_led.setStyleSheet(
                'background-color: green;border: 2px solid black;border-radius: 7px;max-width: 14px;max-height: 14px;')
        elif payload['function'] == 'off':
            self.is_connected_led.setStyleSheet(
                'background-color: red;border: 2px solid black;border-radius: 7px;max-width: 14px;max-height: 14px;')

    def get_gui(self):
        group = QGroupBox('OpalKelly FPGA')
        layout = QHBoxLayout()
        self.is_connected_led = QLabel()
        self.is_connected_led.setStyleSheet(
            'background-color: red;border: 2px solid black;border-radius: 7px;max-width: 14px;max-height: 14px;')
        layout.addWidget(self.is_connected_led)
        connect_button = QPushButton('Connect')
        connect_button.clicked.connect(
            lambda checked: router.route('aihfdoaousadpgfpef',
                                         {'function': 'connect'}
                                         )
        )
        layout.addWidget(connect_button)
        disconnect_button = QPushButton('Disconnect')
        disconnect_button.clicked.connect(
            lambda checked: router.route('aihfdoaousadpgfpef',
                                         {'function': 'disconnect'}
                                         )
        )
        layout.addWidget(disconnect_button)
        # layout.addStretch(1)
        group.setLayout(layout)

        return group
