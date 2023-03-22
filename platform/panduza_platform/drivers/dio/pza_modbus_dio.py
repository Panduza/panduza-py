import time
from ...meta_drivers.dio import MetaDriverDio
from collections import ChainMap
from ...connectors.modbus_client_serial import ConnectorModbusClientSerial



DIO_USBID_VENDOR="16c0"
DIO_USBID_MODEL="05e1"
DIO_TTY_BASE="/dev/ttyACM0"
DIO_USB_BAUDRATE=112500

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
        settings = dict() if "settings" not in tree else tree["settings"]
        settings["vendor"] = DIO_USBID_VENDOR
        settings["model"] = DIO_USBID_MODEL
        settings["base_devname"] = DIO_TTY_BASE
        settings["baudrate"] = DIO_USB_BAUDRATE

        self.modbus_connector = ConnectorModbusClientSerial.GetV2(**settings) # init the connector

        # first configuration
        self.__dir = {
            "direction":{
                "value":"in",
                "pull": "down", 
                "polling_cycle":5
            },
            "state":{
                "active":True,
                "active_low":True,
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
    
    def _PZADRV_DIO_set_direction_value(self, v):
        self.log.info(f"set direction value : {v}")
        self.__dir["direction"]["value"] = v
    
    def _PZADRV_DIO_get_direction_pull(self):
        self.log.info(f"read direction pull : {self.__dir['direction']['pull']}!")
        return self.__dir["direction"]["pull"]

    def _PZADRV_DIO_set_direction_pull(self, v):
        self.log.info(f"set direction pull : {v}")
        self.__dir["direction"]["pull"] = v
    
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