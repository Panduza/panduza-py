from .fake_dio_controller import DevicePanduzaFakeDioController
from .fake_psu_controller import DevicePanduzaFakePsu
from .fake_relay_controller import DevicePanduzaFakeRelayController

PZA_DEVICES_LIST= [ 
    DevicePanduzaFakeDioController,
    DevicePanduzaFakePsu,
    DevicePanduzaFakeRelayController
]
