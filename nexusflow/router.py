from PySide6.QtCore import QObject, Qt, Signal, Slot
from nexusflow.utils import string_uuid

routes = {}


def register_route(destination_id: str, destination_callback: callable):
    routes[destination_id] = destination_callback


def route(destination_id: str, payload: dict):
    routes[destination_id](payload)
