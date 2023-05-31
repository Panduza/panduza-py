
# from .drivers.dio import PZA_DRIVERS_LIST as DRIVERS_DIO
# from .drivers.psu import PZA_DRIVERS_LIST as DRIVERS_PSU


from .drivers.std.driver_platform import DriverPlatform

from .drivers.fake.driver_psu import DriverPsuFake



PZA_DRIVERS_LIST= [
    DriverPlatform,
    DriverPsuFake
]


# =============================================================================

from .devices.panduza.fake_psu import DevicePanduzaFakePsu


PZA_DEVICES_LIST= [ 
    DevicePanduzaFakePsu
]

