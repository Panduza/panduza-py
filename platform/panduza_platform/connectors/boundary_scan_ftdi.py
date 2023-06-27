import asyncio

from panduza_platform.log.driver import driver_logger
from .boundary_scan_base import ConnectorBoundaryScanBase


class ConnectorBoundaryScanFtdi(ConnectorBoundaryScanBase):
    """The serial modbus client connector centralize access to a given port as a modbus client
    """

    # Hold instances mutex
    __MUTEX = asyncio.Lock()

    # Contains instances
    __INSTANCES = {}

    # Local logs
    log = driver_logger("ConnectorBoundaryScanFtdi")




