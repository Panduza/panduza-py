
# from .drivers.dio import PZA_DRIVERS_LIST as DRIVERS_DIO
# from .drivers.psu import PZA_DRIVERS_LIST as DRIVERS_PSU


from .drivers.fake.driver_psu import DriverPsuFake

PZA_DRIVERS_LIST= [ 
    DriverPsuFake
]


from .devices.panduza.fake_psu import DevicePanduzaFakePsu


PZA_DEVICES_LIST= [ 
    DevicePanduzaFakePsu
]

