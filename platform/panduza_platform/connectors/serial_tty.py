import logging
import asyncio
import serial
import serial_asyncio

from .serial_base import ConnectorUartBase
from log.driver import driver_logger

from .udev_tty import SerialPortFromUsbSetting

class ConnectorUartSerial(ConnectorUartBase):
    """
    """

    # Hold instances mutex
    __MUTEX = asyncio.Lock()

    # Contains instances
    __INSTANCES = {}

    # Local logs
    log = driver_logger("ConnectorUartSerial")

    ###########################################################################
    ###########################################################################

    @staticmethod
    async def Get(loop,**kwargs):
        """Singleton main getter

        
        :Keyword Arguments:
        * *serial_port_name* (``str``) --
            serial port name
    
        * *serial_baudrate* (``int``) --
            serial baudrate
            
        * *usb_vendor* (``str``) --
            ID_VENDOR_ID
        * *usb_model* (``str``) --
            ID_MODEL_ID
        """
        # Log
        ConnectorUartSerial.log.debug(f"Get connector for {kwargs}")

        async with ConnectorUartSerial.__MUTEX:

            # Log
            ConnectorUartSerial.log.debug(f"Lock acquired !")


            # Get the serial port name
            serial_port_name = None
            if "serial_port_name" in kwargs:
                serial_port_name = kwargs["serial_port_name"]
            elif "usb_vendor" in kwargs:
                # Get the serial port name using "usb_vendor"
                serial_port_name = SerialPortFromUsbSetting(**kwargs)
                kwargs["serial_port_name"] = serial_port_name
        
            else:
                raise Exception("no way to identify the serial port")

            # Create the new connector
            if not (serial_port_name in ConnectorUartSerial.__INSTANCES):
                ConnectorUartSerial.__INSTANCES[serial_port_name] = None
                try:
                    new_instance = ConnectorUartSerial(loop,**kwargs)
                    await new_instance.connect()
                    
                    ConnectorUartSerial.__INSTANCES[serial_port_name] = new_instance
                    ConnectorUartSerial.log.info("connector created")
                except Exception as e:
                    ConnectorUartSerial.__INSTANCES.pop(serial_port_name)
                    raise Exception('Error during initialization').with_traceback(e.__traceback__)

            # Return the previously created
            return ConnectorUartSerial.__INSTANCES[serial_port_name]

    ###########################################################################
    ###########################################################################

    def __init__(self, loop,**kwargs):
        """Constructor
        """
        # Init local mutex
        self._mutex = asyncio.Lock()
        
        key = kwargs["serial_port_name"]
        
        self.loop = loop
        
        if not (key in ConnectorUartSerial.__INSTANCES):
            raise Exception("You need to pass through Get method to create an instance")
        else:
            self.log = logging.getLogger(key)
            self.log.info(f"attached to the UART Serial Connector")

            
            # Configuration for UART communication

            self.port_name = kwargs.get("serial_port_name", "/dev/ttyUSB0")
            self.baudrate = kwargs.get("serial_baudrate", 9600)


    # ---

    async def connect(self):
        """Start the serial connection
        """

        self.reader,self.writer = await serial_asyncio.open_serial_connection(loop = self.loop,url=self.port_name, baudrate=self.baudrate)
        


    ###########################################################################
    ###########################################################################


    async def read_uart(self, n_bytes = None):
        """Read from UART using asynchronous mode
        """
        
        async with self._mutex:
            #await asyncio.sleep(1)
            try:
                if n_bytes is None:
                    data = await asyncio.wait_for(self.reader.readline(), timeout=1.0)
                else:
                    data = await asyncio.wait_for(self.reader.readexactly(n_bytes), timeout=1.0)
                    print(f"Read data: {data}, Type: {type(data)}")  # Debugging print
                return data
            
            except asyncio.TimeoutError as e: 
                raise Exception('Error during reading uart').with_traceback(e.__traceback__)

    ###########################################################################
    ###########################################################################

    async def write_uart(self,message):
        """write to UART using asynchronous mode
        """
        async with self._mutex:
            #await asyncio.sleep(1)
            try:
                self.writer.write(message.encode())
                await self.writer.drain()
            except Exception as e:
                raise Exception('Error during writing to uart').with_traceback(e.__traceback__)


    ###########################################################################
    # SERIAL SYNCHRONOUS
    ###########################################################################



    # async def connect(self):
    #         """Start the serial connection
    #         """

    #         self.uart = serial.Serial(self.port_name, baudrate=self.baudrate, timeout=1)




    # async def read_uart(self):
    #     async with self._mutex:
    
    #         data = self.uart.readline()[:-2]

    #         decoded_data = data.decode('utf-8')
    #         if decoded_data :
    #             return decoded_data
    


    # async def write_uart(self,message):
    #     async with self._mutex:
    #         print(message.encode())
           
    #         self.uart.write(message.encode())
