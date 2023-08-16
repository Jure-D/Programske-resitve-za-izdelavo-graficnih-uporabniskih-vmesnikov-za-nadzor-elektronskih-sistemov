import logging
from PySide6.QtWidgets import QWidget
from nexusflow.systemdesigner.module.pindefinition import PinDefinition

logging.basicConfig(level=logging.DEBUG)

predefined_components_with_gui = {}


def register_predefined_gui_component(widget_name, data):
    logging.debug(f"Registering widget for {widget_name}")
    predefined_components_with_gui[widget_name] = data


def get_predefined_gui_components():
    return predefined_components_with_gui
