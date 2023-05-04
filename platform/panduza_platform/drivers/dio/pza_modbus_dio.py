import time
from ...meta_drivers.dio import MetaDriverDio
from collections import ChainMap
from ...connectors.modbus_client_serial import ConnectorModbusClientSerial



DIO_USBID_MODEL="05e1"
DIO_USBID_VENDOR="16c0"
DIO_USB_BAUDRATE=112500

DIO_MODBUS_ADDR=1
DIO_OFFSET_PULLS = 32
DIO_OFFSET_WRITE = 64

class DriverPZA_MODBUS_DIO(MetaDriverDio):

    def _PZADRV_config(self):
        # Extend the common psu config
        return ChainMap(
            super()._PZADRV_config(),
            {
                "name": "io_control",
                "description": "Virtual DIO", 
                "compatible": ["pza_modbus_dio","io_pza_controling", "py.pza_modbus_dio"], # name to put in the tree.json
            },
        )

    def _PZADRV_loop_init(self, tree):
        """Driver initialization
        """
        self.log.warning("inside loop init of driver")
        # Load tree settings

        self.settings = dict() if "settings" not in tree else tree["settings"]
        self.settings["vendor"] = DIO_USBID_VENDOR
        self.settings["model"] = DIO_USBID_MODEL
        self.settings["baudrate"] = DIO_USB_BAUDRATE
        self.settings["usb_serial_id"]
        self.settings["gpio_id"]
        
        self.modbus = ConnectorModbusClientSerial.GetV2(**self.settings) # init the connector



        self.direction = False
        self.pullUp = ""
        self.pullDown = ""
        self.turnOn = False
        self.readValue = False

        self.log.info(tree["settings"])

        # first configuration
        self.__dir = {
            "direction":{
                "value":"in",
                "pull": "down", 
                "polling_cycle":1
            },
            "state":{
                "active":False,
                "active_low":False,
                "polling_cycle":1
            }    
        }
        super()._PZADRV_loop_init(tree)


    def _PZADRV_DIO_get_direction_value(self):
        self.log.info(f"read direction value : {self.__dir['direction']['value']} !")
        
        id = self.settings["gpio_id"]        
        self.log.warning(id)
        return self.__dir["direction"]["value"]

    # configure the direction and value of io 
    def _PZADRV_DIO_set_direction_value(self, v): # vlaue direction (in/out)
        self.log.info(f"set direction value : {v}")
        self.__dir["direction"]["value"] = v

        gpio_id = self.settings["gpio_id"] # get the gpio_id number

        if v == "out":    
            self.log.info(f"it's a output")
            self.direction = self.modbus.write_coil(int(gpio_id),True,DIO_MODBUS_ADDR)
            self.log.warning(f"value of output {self.direction}")
        elif v == "in":
            self.log.info("configuration as input")
            self.direction = self.modbus.write_coil(int(gpio_id),False,DIO_MODBUS_ADDR)
            self.log.warning(f"value of input {self.direction}")
        else:
            self.log.warning("unexpected string for DIRECTION")

    def _PZADRV_DIO_set_direction_pull(self, v):
        self.log.info(f"set direction pull : {v}")
        self.__dir["direction"]["pull"] = v # update brocker

        gpio_id = self.settings["gpio_id"]
        if self.__dir["direction"]["pull"]  == "up" and self.direction == False: # False => not a output
            self.log.debug("configuration as pull up")
            self.pullUp = self.modbus.write_coil(int(gpio_id)+DIO_OFFSET_PULLS, True,DIO_MODBUS_ADDR)
        elif self.__dir["direction"]["pull"]  == "down" and self.direction == False : # False => not a output
            self.log.debug("configuration as pull down")
            self.pullDown = self.modbus.write_coil(int(gpio_id)+DIO_OFFSET_PULLS, False,DIO_MODBUS_ADDR)
        else : 
            self.log.warning("you cant set pull for a output")

    def _PZADRV_DIO_get_direction_pull(self):
        self.log.info(f"read direction pull : {self.__dir['direction']['pull']}!")
        return self.__dir["direction"]["pull"]
        
    def _PZADRV_DIO_get_state_active(self):
        self.log.info(f"read state active : {self.__dir['state']['active']}!")
        valueio_0 = self.modbus._ConnectorModbusClientSerial__instances.get("value_i0")
        valueio_2 = self.modbus._ConnectorModbusClientSerial__instances.get("value_i2")
        activeLow = self.modbus._ConnectorModbusClientSerial__instances.get("active_low")
        
        if int(self.settings["gpio_id"]) == 1:
            self.__dir["state"]["active"] = valueio_0
            self.__dir["state"]["active_low"] = activeLow
        elif int(self.settings["gpio_id"]) == 3:
            self.__dir["state"]["active"] = valueio_2
            self.__dir["state"]["active_low"] = activeLow                
        return self.__dir["state"]["active"]
    
    def _PZADRV_DIO_set_state_active(self,v):
        self.log.info(f"set state active : {v}")
        self.__dir["state"]["active"] = v

        gpio_id = self.settings["gpio_id"]
        if self.direction == True and (v == True and self.__dir["state"]["active_low"] == False):
            self.log.warning("OKAY TO WRITE")
            self.turnOn = self.modbus.write_coil(DIO_OFFSET_WRITE+int(gpio_id),v,DIO_MODBUS_ADDR)  # write to coil
            self.readValue = self.modbus.read_discrete_inputs(int(gpio_id)+1,1,DIO_MODBUS_ADDR) # read the input value
            self.modbus._ConnectorModbusClientSerial__instances[f"value_i{int(gpio_id)}"] = self.readValue
            # self.modbus._ConnectorModbusClientSerial__instances.update({f"value_i{int(gpio_id)}": self.readValue})
            self.modbus._ConnectorModbusClientSerial__instances["active_low"] = self.__dir["state"]["active_low"]

        elif self.direction == True and (v == False and self.__dir["state"]["active_low"] == False):
            self.turnOn = self.modbus.write_coil(DIO_OFFSET_WRITE+int(gpio_id),v,DIO_MODBUS_ADDR)  # write to coil
            self.readValue = self.modbus.read_discrete_inputs(int(gpio_id)+1,1,DIO_MODBUS_ADDR) # read the input value
            self.modbus._ConnectorModbusClientSerial__instances[f"value_i{int(gpio_id)}"] = self.readValue
            # self.modbus._ConnectorModbusClientSerial__instances.update({f"value_i{int(gpio_id)}": self.readValue})
            self.modbus._ConnectorModbusClientSerial__instances["active_low"] = self.__dir["state"]["active_low"]

        elif self.direction == True and (v == False and self.__dir["state"]["active_low"] == True): 
            invert = not v
            self.turnOn = self.modbus.write_coil(DIO_OFFSET_WRITE+int(gpio_id),invert,DIO_MODBUS_ADDR) 
            self.readValue = self.modbus.read_discrete_inputs(int(gpio_id)+1,1,DIO_MODBUS_ADDR) # read the input value
            self.modbus._ConnectorModbusClientSerial__instances[f"value_i{int(gpio_id)}"] = self.readValue
            # self.modbus._ConnectorModbusClientSerial__instances.update({f"value_i{int(gpio_id)}": self.readValue})
            self.modbus._ConnectorModbusClientSerial__instances["active_low"] = self.__dir["state"]["active_low"]
        
        elif self.direction == True and (v == True and self.__dir["state"]["active_low"] == True):
            invert = not v
            self.turnOn = self.modbus.write_coil(DIO_OFFSET_WRITE+int(gpio_id),invert,DIO_MODBUS_ADDR) 
            self.readValue = self.modbus.read_discrete_inputs(int(gpio_id)+1,1,DIO_MODBUS_ADDR) # read the input value
            self.modbus._ConnectorModbusClientSerial__instances[f"value_i{int(gpio_id)}"] = self.readValue
            # self.modbus._ConnectorModbusClientSerial__instances.update({f"value_i{int(gpio_id)}": self.readValue})
            self.modbus._ConnectorModbusClientSerial__instances["active_low"] = self.__dir["state"]["active_low"]

        elif self.direction == False:    
            self.log.warning("you can't write a output")

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