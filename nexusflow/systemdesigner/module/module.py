import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QTabWidget, QListWidget, QAbstractItemView

from nexusflow.systemdesigner.excelimport import import_excel
from nexusflow.systemdesigner.module.hwfunction import HWFunction
from nexusflow.systemdesigner.module.predefinedwidgetmanager import register_predefined_gui_component

logging.basicConfig(level=logging.DEBUG)


class Module(QWidget):
    def __init__(self, name: str):
        self.name = name
        self.pin_definitions = []
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.hw_functions_list = QListWidget()
        self.hw_functions_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.hw_functions_list.setFixedWidth(200)
        # self.hw_functions_list.addItems([function.id for function in self.modules[self.module_tabs.currentIndex()]])
        self.hw_functions_list.itemSelectionChanged.connect(self.display_functions)
        self.main_layout.addWidget(self.hw_functions_list)
        self.scroll_area = QScrollArea()
        # self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    def import_functions(self, module_data: List[Any]):
        for function in module_data:
            self.hw_functions_list.addItem(function.id)
            self.pin_definitions.append(HWFunction(function))
            self.scroll_area_layout.addWidget(self.pin_definitions[-1])

    def display_functions(self):
        for function in self.pin_definitions:
            function.hide()
        for function in self.hw_functions_list.selectedItems():
            self.pin_definitions[self.hw_functions_list.indexFromItem(function).row()].show()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_layout.insertStretch(-1)


class ModuleManager(QTabWidget):
    def __init__(self):
        super().__init__()
        # self.setTabsClosable(True)
        # self.tabCloseRequested.connect(self.close_tab_handler)
        self.setMovable(True)
        self.setUsesScrollButtons(True)
        # self.setDocumentMode(True)

    def import_functions(self, path: str) -> None:
        """ Import a module from a path

        :param path: The path to the module
        :type path: str
        """
        module_data = import_excel(path)
        new_module = Module(Path(path).stem)
        new_module.import_functions(module_data)
        register_predefined_gui_component(new_module.name, new_module)
        register_predefined_gui_component(new_module.name+'-important', new_module)
        self.addTab(new_module, new_module.name)

    def get_default_gui_items(self):
        """ Get the default gui items for a module
        """
        for module_index in range(self.count()):
            print(self.widget(module_index))
