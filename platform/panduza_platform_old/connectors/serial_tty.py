import serial
import logging
from .serial_base import ConnectorSerialBase
from .udev_tty import SerialPortFromUsbSetting

class ConnectorSerialTty(ConnectorSerialBase):
    """
    """


    # Contains instances
    __instances = {}

    ###########################################################################
    ###########################################################################

    @staticmethod
    def Get(**kwargs):
        """Singleton main getter
        """
        # Get the serial port name
        port_name = None
        if "port_name" in kwargs:
            port_name = kwargs["port_name"]
        elif "vendor" in kwargs:
            port_name = SerialPortFromUsbSetting(**kwargs)
            kwargs["port_name"] = port_name
        else:
            raise Exception("no way to identify the serial port")


        # Create the new connector
        if not (port_name in ConnectorSerialTty.__instances):
            ConnectorSerialTty.__instances[port_name] = None
            # try:
            new_instance = ConnectorSerialTty(**kwargs)
            ConnectorSerialTty.__instances[port_name] = new_instance
            # except Exception as e:
            #     ConnectorSerialTty.__instances.pop(port_name)
            #     raise Exception('Error during initialization').with_traceback(e.__traceback__)

        # Return the previously created
        return ConnectorSerialTty.__instances[port_name]


    ###########################################################################
    ###########################################################################

    def __init__(self, **kwargs):
        """Constructor
        """

        port_name = kwargs["port_name"]
        if not (port_name in ConnectorSerialTty.__instances):
            raise Exception("You need to pass through Get method to create an instance")
        else:
            self.log = logging.getLogger(port_name)
            self.log.info(f"attached to the Serial TTY Connector")

            self.__internal_driver                  = serial.serial_for_url(port_name, do_not_open=True)
            self.__internal_driver.baudrate         = 19200 if "baudrate" not in kwargs else kwargs["baudrate"]
            self.__internal_driver.bytesize         = serial.EIGHTBITS
            self.__internal_driver.parity           = serial.PARITY_NONE
            self.__internal_driver.stopbits         = serial.STOPBITS_ONE
            self.__internal_driver.rtscts           = False
            self.__internal_driver.timeout          = 10
            self.__internal_driver.write_timeout    = 10

            # Open
            self.__internal_driver.open()


    def read(self):
        pass

    def write(self, data):
        pass


    def get_internal_driver(self):
        return self.__internal_driver

