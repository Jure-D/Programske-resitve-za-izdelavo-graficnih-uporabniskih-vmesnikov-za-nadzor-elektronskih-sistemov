from typing import Protocol
from PySide6.QtWidgets import QLabel, QLCDNumber
from PySide6.QtCore import Slot


class Output(Protocol):
    def update_value(self, value: any) -> None:
        ...


class Label(QLabel):
    def __init__(self, text: str):
        super().__init__()
        self.setText(text)

    @Slot(str)
    def update_value(self, value: str) -> None:
        self.setText(str(value))


class IntLCD(QLCDNumber):
    def __init__(self, value: int):
        super().__init__()
        self.setMode(QLCDNumber.Dec)
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setFrameStyle(QLCDNumber.NoFrame)
        self.display(value)

    @Slot(int)
    def update_value(self, value: int) -> None:
        self.display(value)


class FloatLCD(QLCDNumber):
    def __init__(self, value: float):
        super().__init__()
        self.setMode(QLCDNumber.Dec)
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setFrameStyle(QLCDNumber.NoFrame)
        self.display(value)

    @Slot(float)
    def update_value(self, value: float) -> None:
        self.display(value)


class LED(QLabel):
    led_colors = {
        'red': 'background-color: red; border-radius: 10px; border: 2px solid black;',
        'green': 'background-color: green; border-radius: 10px; border: 2px solid black;',
        'yellow': 'background-color: yellow; border-radius: 10px; border: 2px solid black;',
        'blue': 'background-color: blue; border-radius: 10px; border: 2px solid black;',
        'off': 'background-color: gray; border-radius: 10px; border: 2px solid black;'
    }

    def __init__(self, on: bool, on_color: str, off_color) -> None:
        """A widget that displays a colored circle.

        :param on: Whether the LED should be on or off.
        :type on: bool

        :raises ValueError: Raised if an invalid color is passed.
        ...
        :raises ValueError: Raised if an invalid color is passed.
        """
        super().__init__()
        # self.setScaledContents(True)

        self.on = on

        if on_color in self.led_colors.keys():
            self.on_color = self.led_colors[on_color]
        else:
            raise ValueError(f"Invalid color: {on_color}")

        if off_color in self.led_colors.keys():
            self.off_color = self.led_colors[off_color]
        else:
            raise ValueError(f"Invalid color: {off_color}")

        if self.on:
            self.setStyleSheet(self.on_color)
        else:
            self.setStyleSheet(self.off_color)

    @Slot()
    def turn_on(self) -> None:
        """Turns the LED on.
        """
        self.on = True
        self.setStyleSheet(self.on_color)

    @Slot()
    def turn_off(self) -> None:
        """Turns the LED off.
        """
        self.on = False
        self.setStyleSheet(self.off_color)

    @Slot()
    def toggle(self) -> None:
        """Toggles the LED on or off.
        """
        if self.on:
            self.turn_off()
        else:
            self.turn_on()

    @Slot(bool)
    def set_on(self, value: bool) -> None:
        """Sets the LED on or off.

        :param value: Whether the LED should be on or off.
        :type value: bool
        """
        self.on = value

        if value:
            self.turn_on()
        else:
            self.turn_off()

    def set_on_color(self, color: str) -> None:
        """Sets the color of the LED.

        :param color: The color of the LED. Can be "blue", "green", "red" or "yellow"
        :type color: str
        ...
        :raises ValueError: Raised if an invalid color is passed.
        """
        if color in self.led_colors.keys():
            self.on_color = self.led_colors[color]
        else:
            raise ValueError(f"Invalid color: {color}")

    def set_off_color(self, color: str) -> None:
        """Sets the color of the LED when it is off.

        :param color: The color of the LED. Can be "blue", "green", "red" or "yellow"
        :type color: str
        ...
        :raises ValueError: Raised if an invalid color is passed.
        """
        if color in self.led_colors.keys():
            self.off_color = self.led_colors[color]
        else:
            raise ValueError(f"Invalid color: {color}")

    def set_colors(self, on_color: str, off_color: str) -> None:
        """Sets the colors of the LED.

        :param on_color: The color of the LED when it is on. Can be "blue", "green", "red" or "yellow"
        :type on_color: str
        :param off_color: The color of the LED when it is off. Can be "blue", "green", "red" or "yellow"
        :type off_color: str
        ...
        :raises ValueError: Raised if an invalid color is passed.
        """
        self.set_on_color(on_color)
        self.set_off_color(off_color)

    def get_on(self) -> bool:
        """Returns whether the LED is on.

        :return: Whether the LED is on.
        :rtype: bool
        """
        return self.on
