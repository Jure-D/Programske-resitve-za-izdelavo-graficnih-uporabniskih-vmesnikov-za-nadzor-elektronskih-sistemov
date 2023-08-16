from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QDialog, QPlainTextEdit, \
    QCheckBox, QComboBox, QFormLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QSpacerItem, QFrame, \
    QTabWidget, QTabBar, QStackedWidget, QToolButton, QMenu, QInputDialog, QMessageBox, QFileDialog, QScrollArea, \
    QSizePolicy, QSpacerItem, QFrame, QTabWidget, QTabBar, QStackedWidget, QToolButton, QMenu, QInputDialog, \
    QMessageBox, QMdiArea, QDoubleSpinBox, QSpinBox, QDoubleSpinBox, QRadioButton, QButtonGroup
from PySide6.QtCore import Qt
from nexusflow.globalconstants import float_range, int_range
from nexusflow.systemdesigner.excelimport import PinDefinition


class HWFunction(QGroupBox):
    def __init__(self, pin_definition: PinDefinition):
        super().__init__()
        self.pin_definition = pin_definition
        self.setTitle(self.pin_definition.id)

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.info_group()
        self.conversion_coefficients_group()
        self.gui_group()
        self.important_gui_group()
        self.value_group()
        self.exponential_group()
        self.alarm_group()
        self.main_layout.setColumnStretch(10, 1)

        self.setVisible(False)

    def info_group(self):
        group = QGroupBox('Info')
        group_layout = QGridLayout()
        name_label = QLabel('Name:')
        name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(name_label, 0, 0)
        name_line_edit = QLineEdit()
        name_line_edit.setText(self.pin_definition.name)
        group_layout.addWidget(name_line_edit, 0, 1)
        function_label = QLabel('Function:')
        function_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(function_label, 1, 0)
        function_value_label = QLabel(self.pin_definition.function)
        # function_value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        group_layout.addWidget(function_value_label, 1, 1)
        unit_label = QLabel('Unit:')
        unit_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(unit_label, 2, 0)
        unit_value_line_edit = QLineEdit()
        unit_value_line_edit.setText(self.pin_definition.unit)
        group_layout.addWidget(unit_value_line_edit, 2, 1)

        active_low_checkbox = QCheckBox('Active Low')
        active_low_checkbox.setChecked(self.pin_definition.active_low)
        group_layout.addWidget(active_low_checkbox, 3, 0, 1, 2)

        dac_range_label = QLabel('DAC Range:')
        dac_range_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(dac_range_label, 4, 0)
        dac_range_spinbox = QDoubleSpinBox()
        dac_range_spinbox.setRange(0, float_range[1])
        dac_range_spinbox.setValue(self.pin_definition.miscellaneous.dac_range)
        group_layout.addWidget(dac_range_spinbox, 4, 1)

        adc_range_label = QLabel('ADC Range:')
        adc_range_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(adc_range_label, 5, 0)
        adc_range_spinbox = QDoubleSpinBox()
        adc_range_spinbox.setRange(0, float_range[1])
        adc_range_spinbox.setValue(self.pin_definition.miscellaneous.adc_range)
        group_layout.addWidget(adc_range_spinbox, 5, 1)

        group.setLayout(group_layout)
        self.main_layout.addWidget(group, 0, 0)

    def conversion_coefficients_group(self):
        group = QGroupBox('Conversion Coefficients')
        group_layout = QGridLayout()
        k_label = QLabel('k:')
        k_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(k_label, 0, 0)
        k_spinbox = QDoubleSpinBox()
        k_spinbox.setRange(float_range[0], float_range[1])
        k_spinbox.setValue(self.pin_definition.conversion_coefficients.k)
        # k_spinbox.setSingleStep(0.1)
        # k_spinbox.setDecimals(2)
        # k_spinbox.valueChanged.connect(self.conversion_coefficient_k_spinbox_handler)
        group_layout.addWidget(k_spinbox, 0, 1)
        c_label = QLabel('C:')
        c_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(c_label, 1, 0)
        c_spinbox = QDoubleSpinBox()
        c_spinbox.setRange(float_range[0], float_range[1])
        c_spinbox.setValue(self.pin_definition.conversion_coefficients.C)
        # self.conversion_coefficient_c_spinbox.setSingleStep(0.1)
        # self.conversion_coefficient_c_spinbox.setDecimals(2)
        # self.conversion_coefficient_c_spinbox.valueChanged.connect(self.conversion_coefficient_c_spinbox_handler)
        group_layout.addWidget(c_spinbox, 1, 1)
        group.setLayout(group_layout)
        self.main_layout.addWidget(group, 0, 4)

    def gui_group(self):
        group = QGroupBox('GUI')
        group.setCheckable(True)
        group.setChecked(self.pin_definition.main_gui.display)
        group.toggled.connect(
            lambda value: setattr(self.pin_definition.main_gui, 'display', value)
        )
        group_layout = QGridLayout()
        x_label = QLabel('column:')
        x_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(x_label, 0, 0)
        x_spinbox = QSpinBox()
        x_spinbox.setValue(self.pin_definition.main_gui.column)
        x_spinbox.valueChanged.connect(
            lambda value: setattr(self.pin_definition.main_gui, 'column', value)
        )
        x_spinbox.setRange(0, int_range[1])
        # self.gui_x_spinbox.valueChanged.connect(self.gui_x_spinbox_handler)
        group_layout.addWidget(x_spinbox, 0, 1)
        y_label = QLabel('row:')
        y_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(y_label, 1, 0)
        y_spinbox = QSpinBox()
        y_spinbox.setValue(self.pin_definition.main_gui.row)
        y_spinbox.valueChanged.connect(
            lambda value: setattr(self.pin_definition.main_gui, 'row', value)
        )
        y_spinbox.setRange(0, int_range[1])
        # self.gui_y_spinbox.valueChanged.connect(self.gui_y_spinbox_handler)
        group_layout.addWidget(y_spinbox, 1, 1)
        group.setLayout(group_layout)
        self.main_layout.addWidget(group, 0, 7)

    def value_group(self):
        group = QGroupBox('Value')
        group_layout = QGridLayout()
        min_label = QLabel('Min:')
        min_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(min_label, 0, 0)
        min_spinbox = QDoubleSpinBox()
        min_spinbox.setRange(float_range[0], float_range[1])
        min_spinbox.setValue(self.pin_definition.value.min)
        # min_spinbox.setSingleStep(0.1)
        # min_spinbox.setDecimals(2)
        # min_spinbox.valueChanged.connect(self.range_min_spinbox_handler)
        group_layout.addWidget(min_spinbox, 0, 1)
        max_label = QLabel('Max:')
        max_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(max_label, 1, 0)
        max_spinbox = QDoubleSpinBox()
        max_spinbox.setRange(float_range[0], float_range[1])
        max_spinbox.setValue(self.pin_definition.value.max)
        # max_spinbox.setSingleStep(0.1)
        # max_spinbox.setDecimals(2)
        # max_spinbox.valueChanged.connect(self.range_max_spinbox_handler)
        group_layout.addWidget(max_spinbox, 1, 1)
        initial_label = QLabel('Initial:')
        initial_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(initial_label, 2, 0)
        initial_spinbox = QDoubleSpinBox()
        initial_spinbox.setRange(float_range[0], float_range[1])
        initial_spinbox.setValue(self.pin_definition.value.initial)
        # initial_spinbox.setSingleStep(0.1)
        # initial_spinbox.setDecimals(2)
        # initial_spinbox.valueChanged.connect(self.initial_value_spinbox_handler)
        group_layout.addWidget(initial_spinbox, 2, 1)
        enable_initial_checkbox = QCheckBox('Enable initial value')
        enable_initial_checkbox.setChecked(self.pin_definition.value.enable_initial)
        # enable_initial_checkbox.stateChanged.connect(self.enable_initial_checkbox_handler)
        group.setLayout(group_layout)
        self.main_layout.addWidget(group, 0, 2)

    def important_gui_group(self):
        group = QGroupBox('Important GUI')
        group.setCheckable(True)
        group.setChecked(self.pin_definition.important_gui.display)
        group_layout = QGridLayout()
        x_label = QLabel('column:')
        x_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(x_label, 0, 0)
        x_spinbox = QSpinBox()
        x_spinbox.setValue(self.pin_definition.important_gui.column)
        x_spinbox.setRange(0, int_range[1])
        # self.important_gui_x_spinbox.valueChanged.connect(self.important_gui_x_spinbox_handler)
        group_layout.addWidget(x_spinbox, 0, 1)
        y_label = QLabel('row:')
        y_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(y_label, 1, 0)
        y_spinbox = QSpinBox()
        y_spinbox.setValue(self.pin_definition.important_gui.row)
        y_spinbox.setRange(0, int_range[1])
        # self.important_gui_y_spinbox.valueChanged.connect(self.important_gui_y_spinbox_handler)
        group_layout.addWidget(y_spinbox, 1, 1)
        group.setLayout(group_layout)
        self.main_layout.addWidget(group, 0, 8)

    def exponential_group(self):
        group = QGroupBox('Exponential')
        group.setCheckable(True)
        group.setChecked(self.pin_definition.exponential.enable)
        group_layout = QGridLayout()
        b_label = QLabel('B:')
        b_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(b_label, 0, 0)
        b_spinbox = QDoubleSpinBox()
        b_spinbox.setRange(float_range[0], float_range[1])
        b_spinbox.setValue(self.pin_definition.exponential.B)
        # b_spinbox.setSingleStep(0.1)
        # b_spinbox.setDecimals(2)
        # b_spinbox.valueChanged.connect(self.exponential_b_spinbox_handler)
        group_layout.addWidget(b_spinbox, 0, 1)
        r0_label = QLabel('R0:')
        r0_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(r0_label, 1, 0)
        r0_spinbox = QDoubleSpinBox()
        r0_spinbox.setRange(float_range[0], float_range[1])
        r0_spinbox.setValue(self.pin_definition.exponential.R0)
        # r0_spinbox.setSingleStep(0.1)
        # r0_spinbox.setDecimals(2)
        # r0_spinbox.valueChanged.connect(self.exponential_r0_spinbox_handler)
        group_layout.addWidget(r0_spinbox, 1, 1)
        t0_label = QLabel('T0:')
        t0_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(t0_label, 2, 0)
        t0_spinbox = QDoubleSpinBox()
        t0_spinbox.setRange(float_range[0], float_range[1])
        t0_spinbox.setValue(self.pin_definition.exponential.T0)
        # t0_spinbox.setSingleStep(0.1)
        # t0_spinbox.setDecimals(2)
        # t0_spinbox.valueChanged.connect(self.exponential_t0_spinbox_handler)
        group_layout.addWidget(t0_spinbox, 2, 1)
        group.setLayout(group_layout)
        self.main_layout.addWidget(group, 0, 6)

    def alarm_group(self):
        group = QGroupBox('Alarm')
        group.setCheckable(True)
        group.setChecked(self.pin_definition.alarm.enable)
        group_layout = QGridLayout()
        above_combobox = QComboBox()
        above_combobox.addItems(['Below', 'Above'])
        above_combobox.setCurrentIndex(self.pin_definition.alarm.above)
        # above_combobox.currentIndexChanged.connect(self.alarm_above_combobox_handler)
        group_layout.addWidget(above_combobox, 0, 0)
        warning_label = QLabel('Warning:')
        warning_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(warning_label, 1, 0)
        warning_spinbox = QDoubleSpinBox()
        warning_spinbox.setRange(float_range[0], float_range[1])
        warning_spinbox.setValue(self.pin_definition.alarm.warning_value)
        # warning_spinbox.setSingleStep(0.1)
        # warning_spinbox.setDecimals(2)
        # warning_spinbox.valueChanged.connect(self.alarm_warning_spinbox_handler)
        group_layout.addWidget(warning_spinbox, 1, 1)
        interlock_label = QLabel('Interlock:')
        interlock_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group_layout.addWidget(interlock_label, 2, 0)
        interlock_spinbox = QDoubleSpinBox()
        interlock_spinbox.setRange(float_range[0], float_range[1])
        interlock_spinbox.setValue(self.pin_definition.alarm.interlock_value)
        # interlock_spinbox.setSingleStep(0.1)
        # interlock_spinbox.setDecimals(2)
        # interlock_spinbox.valueChanged.connect(self.alarm_interlock_spinbox_handler)
        group_layout.addWidget(interlock_spinbox, 2, 1)
        group.setLayout(group_layout)
        self.main_layout.addWidget(group, 0, 9)
