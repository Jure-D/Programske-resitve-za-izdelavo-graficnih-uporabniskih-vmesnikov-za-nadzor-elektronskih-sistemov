from typing import Callable
from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, text: str, callback: Callable):
        """A button widget that can be clicked.

        :param text: The text to display on the button.
        :type text: str
        :param callback: The function to call when the button is clicked.
        :type callback: Callable
        """
        super().__init__()
        self.setText(text)
        self.clicked.connect(callback)
