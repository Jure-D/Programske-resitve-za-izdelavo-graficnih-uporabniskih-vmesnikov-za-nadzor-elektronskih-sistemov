from PySide6.QtCore import QObject
from pathlib import Path
from nexusflow.systemdesigner.controllers import fpga
from nexusflow.utils import string_uuid
from nexusflow import router


def ic_mapper(ic_id: str):
    if ic_id[:3] == 'ADD':
        ic_id.replace('ADD', '')
        ic_id_split = ic_id.split(' ')
        if ic_id[0] == '1':
            return 0, int(ic_id_split[1])
        elif ic_id[0] == '3':
            return 1, int(ic_id_split[1])
        elif ic_id[0] == '4':
            return 2, int(ic_id_split[1])
        else:
            raise ValueError(f"Invalid IC ID {ic_id}")


class OKFPGAController(QObject):
    def __init__(self):
        super().__init__()
        self.uuid = string_uuid()
        self.name = "Opal Kelly FPGA"
        self.bitfile = 'C:/Users/aspus/Desktop/nexusflow/nexusflow/systemdesigner/controllers/fpga/bitfiles/xem7310_flc5.0_200_160MHz_11_05_2022.bit'
        self.fpga = None
        self.modules = {}

        self.register_route()

    def init(self):
        self.fpga = fpga.FPGAController(self.bitfile)
        router.route(destination_id='asdoncdsajcbds', payload={'function': 'on'})
        self.add_module('')

    def add_module(self, module_excel_path: str):
        self.modules['ADD_adapter_test'] = self.fpga.add_module("C:/Users/aspus/Desktop/ADD_adapter_test.xlsm")

    def disconnect(self):
        del self.fpga
        router.route(destination_id='asdoncdsajcbds', payload={'function': 'off'})

    def register_route(self):
        # router.register_route(self.uuid, self.handle_route)
        router.register_route('aihfdoaousadpgfpef', self.handle_route)

    def handle_route(self, payload: dict):
        if payload['id'] == 'fpga':
            if  payload['function'] == 'connect':
                self.init()
            elif payload['id'] == 'disconnect':
                self.disconnect()
        elif payload['id'][:3] == 'ADD':
            data = payload['id'].replace('ADD', '')
            data = data.split(' ')
            channel_index = int(data[1])
            if data[0] == '1':
                device_index = 0
            elif data[0] == '3':
                device_index = 1
            elif data[0] == '4':
                device_index = 2
            else:
                raise ValueError(f"Invalid IC ID {payload['id']} for ADD")

            if payload['function'] == 'DIG_OUT':
                self.modules['ADD_adapter_test'].adds[device_index].write_digital(channel_index, payload['value'])
        # elif payload['id'][:3] == 'DAC':
        #     pass
        # elif payload['id'][:2] == 'DG':




