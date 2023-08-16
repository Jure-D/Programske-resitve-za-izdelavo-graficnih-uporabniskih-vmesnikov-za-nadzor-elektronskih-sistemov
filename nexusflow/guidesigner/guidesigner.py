from typing import List
import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QTabWidget, QTreeWidget, QGroupBox, QPushButton, \
    QHBoxLayout, QDialog, QLineEdit, QDialogButtonBox, QLabel, QTreeWidget, QTreeWidgetItem, QComboBox
from PySide6.QtCore import Qt, Signal, Slot

from nexusflow.guidesigner.guiitems import GuiContainerItem, GuiInputWidgetItem, GuiOutputWidgetItem, \
    GuiControllerWidgetItem
from nexusflow import router
from nexusflow.systemdesigner.module.predefinedwidgetmanager import get_predefined_gui_components
from nexusflow.systemdesigner.controllers.okfpga import OKFPGAController
from nexusflow.systemdesigner.module.module import Module

logging.basicConfig(level=logging.DEBUG)


class PanelWidget(QTreeWidget):
    statusbar_message = Signal(str)

    def __init__(self, panel_type: str = None):
        super().__init__()
        self.panel_type = panel_type
        self.setHeaderLabels(["Name", "Type"])
        self.itemClicked.connect(self.click_handler)
        self.itemDoubleClicked.connect(self.item_double_click_handler)

        self.editor_in: List[QTreeWidgetItem, int] = []
        self.item_selected: bool = False

    @Slot(QTreeWidgetItem, int)
    def item_double_click_handler(self, item: QTreeWidgetItem, column: int):
        item.show_settings_dialog()

    @Slot(QTreeWidgetItem, int)
    def click_handler(self, item: QTreeWidgetItem, column: int):
        if self.item_selected:
            self.setCurrentItem(None)
            self.item_selected = False
        else:
            self.setCurrentItem(item)
            self.item_selected = True

    def add_widget(self, widget: QTreeWidgetItem):
        # Adding item to root
        if self.currentItem() is None:
            if self.topLevelItemCount() >= 1:
                self.statusbar_message.emit("There can only be one top level widget")
                return

            self.addTopLevelItem(widget)
            logging.debug(f"Adding {widget} to root")
            return

            # If container is selected add widget to it
        if not isinstance(self.currentItem(), GuiContainerItem):
            self.currentItem().setExpanded(True)
            self.statusbar_message.emit("There can only be one top level widget")
            return
        # If widget is selected add widget to parent container
        logging.debug(f"Adding {widget} to {self.currentItem()}")
        self.currentItem().addChild(widget)

    def remove_widget(self):
        if self.currentItem().parent() is not None:
            self.currentItem().parent().removeChild(self.currentItem())
        else:
            self.clear()

    def add_predefined_gui_components(self, module: Module, important: bool):
        if isinstance(module, OKFPGAController):
            widget = GuiControllerWidgetItem()
            self.add_widget(widget)
        else:
            logging.debug(f'Adding {"important " if important else ""}GUI for {module.name}')
            container = GuiContainerItem()
            container.name.name = f'{module.name}{"-important" if important else ""}'
            container.generate_type_description()
            for pin_definition in module.pin_definitions:
                if (pin_definition.pin_definition.main_gui.display and not important) or \
                        (important and pin_definition.pin_definition.important_gui.display):

                    dict_factory = {
                        'input': GuiInputWidgetItem,
                        'output': GuiOutputWidgetItem
                    }
                    try:
                        editor = dict_factory[pin_definition.pin_definition.main_gui.display_direction]()
                        editor.add_data(pin_definition.pin_definition, is_important=important)
                    except KeyError:
                        raise ValueError(f'Could not determine if {pin_definition.pin_definition.function}' +
                                         ' is input or output.')

                    # if pin_definition.pin_definition.main_gui.display_direction == 'input':
                    #     editor = GuiInputWidgetItem()
                    #     editor.add_data(pin_definition.pin_definition, is_important=important)
                    # elif pin_definition.pin_definition.main_gui.display_direction == 'output':
                    #     editor = GuiOutputWidgetItem()
                    #     editor.add_data(pin_definition.pin_definition, is_important=important)
                    # else:
                    #     raise ValueError(f'Could not determine if {pin_definition.pin_definition.function}' +
                    #                      ' is input or output.')
                    container.addChild(editor)
            self.add_widget(container)

    def get_gui(self) -> QWidget:
        if self.topLevelItemCount() > 0:
            return self.topLevelItem(0).get_gui()
        else:
            raise Exception("No top level widget")


class PanelTabs(QTabWidget):
    statusbar_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.setTabsClosable(False)
        self.tabBarDoubleClicked.connect(self.tab_bar_double_clicked_handler)

    def add_tab(self, panel_widget, name):
        self.addTab(panel_widget, name)
        self.currentWidget().statusbar_message.connect(self.statusbar_message.emit)

    def tab_bar_double_clicked_handler(self, index: int):
        dialog = QDialog()
        dialog.setWindowTitle("Add panel")
        dialog_layout = QGridLayout()
        name_label = QLabel("Name:")
        name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        dialog_layout.addWidget(name_label, 0, 0)
        name_input = QLineEdit()
        name_input.setText(f"{self.tabText(index)}")
        dialog_layout.addWidget(name_input, 0, 1)
        dialog_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_button_box.accepted.connect(dialog.accept)
        dialog_button_box.rejected.connect(dialog.reject)
        dialog_layout.addWidget(dialog_button_box, 1, 0, 1, 2)
        dialog.setLayout(dialog_layout)

        if dialog.exec_() == QDialog.Accepted:
            self.setTabText(index, name_input.text())


class GuiDesigner(QWidget):
    statusbar_message = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.panels = []

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.top_bar()

        self.gui_panel_tabs = PanelTabs()
        self.main_layout.addWidget(self.gui_panel_tabs)

    def top_bar(self):
        self.top_bar_widget = QWidget()
        self.top_bar_layout = QHBoxLayout()

        self.predefined_gui_group()
        self.widgets_group()
        self.top_bar_layout.insertStretch(2, stretch=2)
        self.panels_group()
        self.run_group()

        self.top_bar_widget.setLayout(self.top_bar_layout)
        self.main_layout.addWidget(self.top_bar_widget)

    def predefined_gui_group(self):
        group = QGroupBox("Predefined GUI components")
        layout = QGridLayout()

        self.predefined_gui_combo = QComboBox()
        self.predefined_gui_combo.setFixedWidth(200)
        self.predefined_gui_combo.addItem("Empty")
        layout.addWidget(self.predefined_gui_combo, 0, 0)
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_handler)
        layout.addWidget(refresh_button, 0, 1)
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_predefined_gui_handler)
        layout.addWidget(add_button, 1, 0, 1, 2)

        layout.setColumnStretch(0, 1)
        group.setLayout(layout)
        self.top_bar_layout.addWidget(group)

    def widgets_group(self):
        widget = QGroupBox("GUI Widgets")
        layout = QVBoxLayout()

        container_button = QPushButton("Container")
        container_button.clicked.connect(self.add_container_handler)
        layout.addWidget(container_button)

        add_input_button = QPushButton("Input")
        add_input_button.clicked.connect(self.add_input_handler)
        layout.addWidget(add_input_button)

        add_output_button = QPushButton("Output")
        add_output_button.clicked.connect(self.add_output_handler)
        layout.addWidget(add_output_button)

        widget.setLayout(layout)
        self.top_bar_layout.addWidget(widget)

    def panels_group(self):
        group = QGroupBox("Panel")
        layout = QVBoxLayout()
        add_panel_button = QPushButton("Add")
        add_panel_button.clicked.connect(self.add_panel_handler)
        layout.addWidget(add_panel_button)
        remove_panel_button = QPushButton("Remove")
        remove_panel_button.clicked.connect(self.remove_panel_handler)
        layout.addWidget(remove_panel_button)
        group.setLayout(layout)
        self.top_bar_layout.addWidget(group)

    def run_group(self):
        group = QGroupBox("Run panels")
        layout = QVBoxLayout()
        show_current_button = QPushButton("Run current")
        show_current_button.clicked.connect(self.run_current_handler)
        layout.addWidget(show_current_button)
        show_all_button = QPushButton("Run all")
        show_all_button.clicked.connect(self.run_all_handler)
        layout.addWidget(show_all_button)
        group.setLayout(layout)
        layout.addWidget(group)
        self.top_bar_layout.addWidget(group)

    def refresh_handler(self):
        self.predefined_gui_combo.clear()
        for module in get_predefined_gui_components().keys():
            self.predefined_gui_combo.addItem(module)

    def add_predefined_gui_handler(self):
        if self.gui_panel_tabs.currentWidget() is None:
            self.statusbar_message.emit('There is no panel to add a widget to.')
        else:
            if self.predefined_gui_combo.currentText() == 'Empty':
                self.statusbar_message.emit('There are no predefined GUI components to add.')
            else:
                if self.predefined_gui_combo.currentText().endswith('-important'):
                    important = True
                    module = get_predefined_gui_components()[self.predefined_gui_combo.currentText()[:-11]]
                else:
                    important = False
                    module = get_predefined_gui_components()[self.predefined_gui_combo.currentText()]
                print(module)
                self.gui_panel_tabs.currentWidget().add_predefined_gui_components(module, important)

    def add_container_handler(self):
        if not self.gui_panel_tabs.currentWidget() is None:
            self.gui_panel_tabs.currentWidget().add_widget(GuiContainerItem())
        else:
            self.statusbar_message.emit('There is no panel to add a widget to.')

    def add_input_handler(self):
        if not self.gui_panel_tabs.currentWidget() is None:
            self.gui_panel_tabs.currentWidget().add_widget(GuiInputWidgetItem())
        else:
            self.statusbar_message.emit('There is no panel to add a widget to.')

    def add_output_handler(self):
        if not self.gui_panel_tabs.currentWidget() is None:
            self.gui_panel_tabs.currentWidget().add_widget(GuiOutputWidgetItem())
        else:
            self.statusbar_message.emit('There is no panel to add a widget to.')

    def add_panel_handler(self):
        dialog = QDialog()
        dialog.setWindowTitle("Add panel")
        dialog_layout = QGridLayout()
        name_label = QLabel("Name:")
        name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        dialog_layout.addWidget(name_label, 0, 0)
        name_input = QLineEdit()
        name_input.setText(f"Panel {self.gui_panel_tabs.count() + 1}")
        dialog_layout.addWidget(name_input, 0, 1)
        dialog_button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_button_box.accepted.connect(dialog.accept)
        dialog_button_box.rejected.connect(dialog.reject)
        dialog_layout.addWidget(dialog_button_box, 1, 0, 1, 2)
        dialog.setLayout(dialog_layout)

        if dialog.exec_() == QDialog.Accepted:
            self.add_panel(name_input.text())

    def add_panel(self, name):
        panel_widget = PanelWidget()
        panel_widget.statusbar_message.connect(self.statusbar_message)
        self.gui_panel_tabs.add_tab(panel_widget, name)

    def remove_panel_handler(self):
        self.gui_panel_tabs.removeTab(self.gui_panel_tabs.currentIndex())

    def remove_widget_handler(self):
        self.gui_panel_tabs.currentWidget().remove_widget()

    def run_current_handler(self):
        self.panels = [self.gui_panel_tabs.currentWidget().get_gui()]
        self.show_gui()

    def run_all_handler(self):
        self.panels = []
        for panel in range(self.gui_panel_tabs.count()):
            self.panels.append(self.gui_panel_tabs.widget(panel).get_gui())
        self.show_gui()

    def show_gui(self):
        for panel in self.panels:
            panel.show()

    def add_widget(self, widget):
        self.panels[self.gui_panel_tabs.currentIndex()].add_widget(widget)
