from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTabWidget, QTreeWidget, QScrollArea, QGroupBox


class AutomationWidget(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Automation 1")


class AutomationsDesigner(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.controls_widget = QWidget()
        self.controls_layout = QGridLayout()
        self.controls_widget.setLayout(self.controls_layout)
        self.main_layout.addWidget(self.controls_widget)

        self.automations_widget = QScrollArea()
        self.main_layout.addWidget(self.automations_widget)
        self.automations_layout = QVBoxLayout()
        self.automations_widget.setLayout(self.automations_layout)
        # self.automations_layout.setAlignment(Qt.AlignTop)

        self.automation_widget = AutomationWidget()
        self.automations_layout.addWidget(self.automation_widget)
