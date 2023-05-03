import time
from ...meta_drivers.dio import MetaDriverDio
from collections import ChainMap
from ...connectors.modbus_client_serial import ConnectorModbusClientSerial



DIO_USBID_MODEL="05e1"
DIO_USBID_VENDOR="16c0"
DIO_USB_BAUDRATE=112500
DIO_MODBUS_ADDR=1
class DriverPZA_MODBUS_DIO(MetaDriverDio):

    def _PZADRV_config(self):
        # Extend the common psu config
        return ChainMap(
            super()._PZADRV_config(),
            {
                "name": "My_Input_Output",
                "description": "Virtual DIO", 
                "compatible": ["pza_modbus_dio", "py.pza_modbus_dio"], # name to put in the tree.json
            },
        )

    def _PZADRV_loop_init(self, tree):
        """Driver initialization
        """
        # settings = tree["settings"]
        # Load settings
        self.settings = dict() if "settings" not in tree else tree["settings"]
        self.settings["vendor"] = DIO_USBID_VENDOR
        self.settings["model"] = DIO_USBID_MODEL
        self.settings["baudrate"] = DIO_USB_BAUDRATE
        self.settings["usb_serial_id"]
        self.settings["gpio_id"]
        
        self.modbus = ConnectorModbusClientSerial.GetV2(**self.settings) # init the connector
        self.log.info(tree["settings"])

        # first configuration
        self.__dir = {
            "direction":{
                "value":"in",
                "pull": "down", 
                "polling_cycle":5
            },
            "state":{
                "active":True,
                "active_low":False,
                "polling_cycle":5
            }    
        }
        
        super()._PZADRV_loop_init(tree) # update tree
    
    def _PZADRV_loop_run(self):
        pass
    def _PZADRV_loop_err(self):
        pass
    
    def _PZADRV_DIO_get_direction_value(self):
        self.log.info(f"read direction value : {self.__dir['direction']['value']} !")
        return self.__dir["direction"]["value"]
    
    # configure the direction and value of io 
    def _PZADRV_DIO_set_direction_value(self, v): # vlaue direction (in/out)
        self.log.info(f"set direction value : {v}")
        self.__dir["direction"]["value"] = v
        gpio_id = self.settings["gpio_id"] # get the gpio_id number
        self.log.debug(f"value of io repeated {gpio_id}")

        if v == "out":    
            self.log.info(f"it's a output")
            self.modbus.write_coil(int(gpio_id),True,DIO_MODBUS_ADDR) # configure output+
            self.modbus.write_coil(64+int(gpio_id),1,DIO_MODBUS_ADDR)  # write to coil
            
            io_controling = self.modbus.read_discrete_inputs(int(gpio_id)+1,1,DIO_MODBUS_ADDR)
            self.log.warning(f"value of IO 1 {io_controling}")
            time.sleep(2)
            self.modbus.write_coil(64+int(gpio_id),False,DIO_MODBUS_ADDR)

    def _PZADRV_DIO_set_direction_pull(self, v):
        self.log.info(f"set direction pull : {v}")
        self.__dir["direction"]["pull"] = v
        # gpio = self.__dir["direction"]["value"]

        # if self.__dir["direction"]["pull"]  == "up":
        #     self.log.info("set gpio as pull up")
        #     self.modbus.write_coil(DIO_USB_GPIO_CONTROL+32, True,DIO_MODBUS_ADDR)
        # elif self.__dir["direction"]["pull"]  == "down":
        #     self.log.info("set gpio as pull down")
        #     self.modbus.write_coil(DIO_USB_GPIO_CONTROL+32, False,DIO_MODBUS_ADDR)

    def _PZADRV_DIO_get_direction_pull(self):
        self.log.info(f"read direction pull : {self.__dir['direction']['pull']}!")
        return self.__dir["direction"]["pull"]
        
    def _PZADRV_DIO_get_state_active(self):
        self.log.info(f"read state active : {self.__dir['state']['active']}!")
        return self.__dir["state"]["active"]
    
    def _PZADRV_DIO_set_state_active(self,v):
        self.log.info(f"set state active : {v}")
        self.__dir["state"]["active"] = v
    
    def _PZADRV_DIO_get_state_activeLow(self):
        self.log.info(f"read state active low : {self.__dir['state']['active_low']}!")
        return self.__dir["state"]["active_low"]
    
    def _PZADRV_DIO_set_state_activeLow(self,v):
        self.log.info(f"set state active low : {v}")
        self.__dir["state"]["active_low"] = v

    def _PZADRV_DIO_get_state_pulling(self):
        self.log.info(f"read state pulling : {self.__dir['state']['polling_cycle']}!")
        return self.__dir["state"]["polling_cycle"]
    
    def _PZADRV_DIO_set_state_pulling(self,v):
        self.log.info(f"set state pulling : {v}")
        self.__dir["state"]["polling_cycle"] = v

    def _PZADRV_DIO_get_direction_pulling(self):
        self.log.info(f"read direction pulling : {self.__dir['direction']['polling_cycle']}!")
        return self.__dir["direction"]["polling_cycle"]
    
    def _PZADRV_DIO_set_direction_pulling(self,v):
        self.log.info(f"set direction pulling : {v}")
        self.__dir["direction"]["polling_cycle"] = v