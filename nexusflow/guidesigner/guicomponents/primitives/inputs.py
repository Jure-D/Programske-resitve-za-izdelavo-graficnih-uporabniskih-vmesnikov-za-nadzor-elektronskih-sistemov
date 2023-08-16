from typing import Optional, Any, Protocol
from PySide6.QtWidgets import QWidget, QGridLayout, QGroupBox, QPushButton, QLabel, QLineEdit, QSpinBox, \
    QDoubleSpinBox, QCheckBox, QComboBox, QDialog, QApplication, QFileDialog, QDialogButtonBox, QPlainTextEdit
from PySide6.QtCore import Qt, Signal
from nexusflow.globalconstants import float_range, int_range

class Input(Protocol):
    def get_value(self) -> Any:
        ...


class StringLineEdit(QLineEdit):
    def __init__(self, value: str):
        """ Widget for editing a string in a single line

        :param value: value to be displayed in the line edit
        :type value: str
        """
        super().__init__()
        self.value = value
        self.setText(self.value)

    def get_value(self) -> str:
        return self.text()


class StringMultiLine(QPlainTextEdit):
    def __init__(self, value: str):
        """ Widget for editing a string in multiple lines

        :param value: value to be displayed in the editor
        :type value: str
        """
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.setPlainText(value)

    def get_value(self) -> str:
        """Returns the value of the editor

        :return: Value of the editor
        :rtype: str
        """
        return self.toPlainText()


class IntSpinBox(QSpinBox):
    def __init__(self,
                 value: int,
                 range_min: Optional[int] = None,
                 range_max: Optional[int] = None,
                 step: Optional[int] = None) -> None:
        """

        :param value: Initial value of the spinbox
        :type value: int
        :param range_min: Minimum value of the spinbox
        :type range_min: int
        :param range_max: Maximum value of the spinbox
        :type range_max: int
        :param step: Step of the spinbox
        :type step: int
        """
        super().__init__()
        if range_min is not None:
            self.setMinimum(range_min)
        else:
            self.setMinimum(int_range[0])
        if range_max is not None:
            self.setMaximum(range_max)
        else:
            self.setMaximum(int_range[1])
        if step is not None:
            self.setSingleStep(step)
        self.setValue(value)
        # self.setSpecialValueText("")

    def get_value(self) -> int:
        """Returns the value of the spinbox

        :return: Value of the spinbox
        :rtype: int
        """
        return self.value()


class FloatSpinBox(QDoubleSpinBox):
    def __init__(self,
                 value: float,
                 range_min: Optional[float] = None,
                 range_max: Optional[float] = None,
                 step: Optional[float] = None) -> None:
        """

        :param value: Initial value of the spinbox
        :type value: float
        :param range_min: Minimum value of the spinbox
        :type range_min: float
        :param range_max: Maximum value of the spinbox
        :type range_max: float
        :param step: Step of the spinbox
        :type step: float
        """
        super().__init__()
        if range_min is not None:
            self.setMinimum(range_min)
        else:
            self.setMinimum(float_range[0])
        if range_max is not None:
            self.setMaximum(range_max)
        else:
            self.setMaximum(float_range[1])
        if step is not None:
            self.setSingleStep(step)
        self.setValue(value)

    def get_value(self) -> float:
        """ Returns the value of the spinbox

        :return: Value of the spinbox
        :rtype: float
        """
        return self.value()


class BoolCheckBox(QCheckBox):
    def __init__(self, value: bool):
        """ Widget for editing a boolean value

        :param value: Initial value of the checkbox
        :type value: bool
        """
        super().__init__()
        self.setChecked(value)

    def get_value(self) -> bool:
        return self.isChecked()


class ListComboBox(QComboBox):
    def __init__(self, value: int, options: list):
        """ Widget for selecting an item from a list

        :param value: Index of the selected item
        :type value: int
        :param options: List of options to select from
        :type options: list
        """
        super().__init__()
        self.addItems(options)
        self.setCurrentIndex(value)

    def get_value(self) -> int:
        """ Returns the index of the selected item

        :return: Index of the selected item
        :rtype: int
        """
        return self.currentIndex()

    def get_value_text(self) -> str:
        """ Returns the text of the selected item

        :return: Text of the selected item
        :rtype: str
        """
        return self.currentText()


class FileSelector(QPushButton):
    def __init__(self, value: str, validator: Optional[str] = None) -> None:
        """ Widget for selecting a file from the file system

        :param value: Path to the selected file
        :type value: str
        :param validator: File type filter
        :type validator: str
        """
        super().__init__()
        self.value = value
        if validator is not None:
            self.validator = validator
        else:
            self.validator = 'All Files (*)'
        self.setText('Browse')
        self.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        """ Opens a file dialog and sets the value of the widget to the selected file
        """
        self.value = QFileDialog.getOpenFileName(self, 'Open file', '', self.validator)[0]

    def get_value(self) -> str:
        """ Returns the value of the widget

        :return: Path to the selected file
        :rtype: str
        """
        return self.value
