from PySide6.QtWidgets import QApplication
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from nexusflow.guidesigner.guicomponents.primitives.containers import LinearContainer, GroupContainer
from nexusflow.guidesigner.guicomponents.primitives.outputs import Label, IntLCD, FloatLCD, LED
from nexusflow.guidesigner.guicomponents.primitives.inputs import StringLineEdit, StringMultiLine, IntSpinBox, \
    ListComboBox, FloatSpinBox, BoolCheckBox, FileSelector
from nexusflow.guidesigner.guicomponents.primitives.triggers import Button

from nexusflow.router import get_router
from nexusflow.toolbox.utils import string_uuid


class MainWindow(LinearContainer):
    def __init__(self):
        super().__init__(layout="vertical")
        self.setWindowTitle("Example")
        # self.resize(500, 500)

        self.layout.addWidget(OutputsExampleGroup())
        self.layout.addWidget(InputsExampleGroup())


class OutputsExampleGroup(GroupContainer):
    def __init__(self):
        super().__init__(title="Outputs", layout="horizontal")

        self.router = get_router()

        self.leds_group()
        self.lcd()
        self.text()

    def leds_group(self):
        # group = GroupContainer(title="LEDs", layout="vertical")
        widget = QGroupBox("LEDs")
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        # layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 20)
        green_label = QLabel("Green")
        green_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(green_label, 0, 0)
        green_led = LED(on=False,
                        on_color='green',
                        off_color='off')
        self.router.register_endpoint('f224337e-3df8-447e-8c62-728789d98024', green_led.toggle)
        layout.addWidget(green_led,
                         0, 1)
        red_label = QLabel("Red")
        red_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(red_label, 1, 0)
        layout.addWidget(LED(on=False,
                             on_color='red',
                             off_color='off', ),
                         1, 1)
        yellow_label = QLabel("Yellow")
        yellow_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(yellow_label, 2, 0)
        layout.addWidget(LED(on=False,
                             on_color='yellow',
                             off_color='off', ),
                         2, 1)
        blue_label = QLabel("Blue")
        blue_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(blue_label, 3, 0)
        layout.addWidget(LED(on=False,
                             on_color='blue',
                             off_color='off', ),
                         3, 1)
        # group.layout.addWidget(LED(on=True,
        #                            on_color='green',
        #                            off_color='off',))
        # group.layout.addWidget(LED(on=True,
        #                            on_color='red',
        #                            off_color='off',))
        # group.layout.addWidget(LED(on=True,
        #                            on_color='yellow',
        #                            off_color='off',))
        # group.layout.addWidget(LED(on=True,
        #                            on_color='blue',
        #                            off_color='off',))

        # self.layout.addWidget(group)
        widget.setLayout(layout)
        self.layout.addWidget(widget)

    def lcd(self):
        group = GroupContainer(title="LCDs", layout="vertical")

        int_lcd = IntLCD(47)
        group.layout.addWidget(int_lcd)

        float_lcd = FloatLCD(4.7)
        group.layout.addWidget(float_lcd)

        self.layout.addWidget(group)

    def text(self):
        group = GroupContainer(title="String", layout="vertical")
        group.layout.addWidget(Label(text='This is text output'))
        self.layout.addWidget(group)


class InputsExampleGroup(GroupContainer):
    def __init__(self):
        super().__init__(title="Inputs", layout="horizontal")

        self.router = get_router()

        self.boolean()
        self.buttons()
        self.numbers()
        self.selectors()
        self.text()

    def boolean(self):
        # group = GroupContainer(title="Boolean", layout="vertical")
        # group.layout.addWidget(BoolCheckBox(value=False))
        # self.layout.addWidget(group)
        widget = QGroupBox("Boolean")
        layout = QGridLayout()
        layout.addWidget(QLabel("RED"), 0, 0)
        red_checkbox = BoolCheckBox(value=False)
        red_checkbox.stateChanged.connect(self.handle_red_checkbox)
        layout.addWidget(red_checkbox, 0, 1)
        widget.setLayout(layout)
        self.layout.addWidget(widget)

    def handle_red_checkbox(self):
        self.router.route(msg={'destination_id': 'f224337e-3df8-447e-8c62-728789d98024'})

    def buttons(self):
        group = GroupContainer(title="Buttons", layout="vertical")
        group.layout.addWidget(Button(
            text='BUTTON',
            callback=lambda: print('Button pressed')))
        self.layout.addWidget(group)

    def numbers(self):
        group = GroupContainer(title="Numbers", layout="vertical")
        group.layout.addWidget(IntSpinBox(
            value=0, range_min=-10, range_max=10, step=1
        ))
        group.layout.addWidget(FloatSpinBox(
            value=0, range_min=-1, range_max=1, step=0.1
        ))
        self.layout.addWidget(group)

    def selectors(self):
        group = GroupContainer(title="Selectors", layout="vertical")
        selector = ListComboBox(
            value=0,
            options=["Option 1", "Option 2", "Option 3"],
        )
        group.layout.addWidget(selector)
        self.layout.addWidget(group)

    def text(self):
        group = GroupContainer(title="String", layout="vertical")
        group.layout.addWidget(StringLineEdit(value='This is text input'))
        group.layout.addWidget(StringMultiLine(value='This is much, much longer text input. To prove the point this text is unnecessarily long.'))
        self.layout.addWidget(group)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
