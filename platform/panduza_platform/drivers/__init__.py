
from .ammeter       import PZA_DRIVERS_LIST as AMMETERS_DRIVERS
from .dio           import PZA_DRIVERS_LIST as DIO_DRIVERS
from .platform      import PZA_DRIVERS_LIST as PLATFORM_DRIVERS
from .bpc           import PZA_DRIVERS_LIST as BPC_DRIVERS
from .relay         import PZA_DRIVERS_LIST as RELAY_DRIVERS
from .voltmeter     import PZA_DRIVERS_LIST as VOLTMETERS_DRIVERS

PZA_DRIVERS_LIST= [] \
    + AMMETERS_DRIVERS \
    + DIO_DRIVERS \
    + PLATFORM_DRIVERS \
    + BPC_DRIVERS \
    + RELAY_DRIVERS \
    + VOLTMETERS_DRIVERS
