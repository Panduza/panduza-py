from ...meta_drivers.dio import MetaDriverDio

class DriverFakeDio(MetaDriverDio):

    # =============================================================================
    # FROM MetaDriverDio

    def _PZA_DRV_DIO_config(self):
        return {
            "name": "panduza.fake.dio",
            "description": "Virtual DIO"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Init function
        Reset fake parameters
        """
        self.__fakes = {
            "direction": {
                "value": "in",
                "pull": "open"
            },
            "state": {
                "active": False,
                "active_low": False
            },
            "settings_capabilities": {
                "ovp": False,       # Over Voltage Protection
                "ocp": False,       # Over Current Protection
                "silent": False,    # Silent mode
            },
        }

        # Call meta class PSU ini
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    def _PZA_DRV_DIO_get_direction_value(self):
        """From MetaDriverDio
        """
        return self.__fakes["direction"]["value"]

    # ---

    def _PZA_DRV_DIO_set_direction_value(self, value):
        """ set value of direction value

        -  Args
            value : value to be set : in or out
        """
        self.__fakes["direction"]["value"] = value

    # ---

    def _PZA_DRV_DIO_get_direction_pull(self):
        """ get direction pull
        """
        return self.__fakes["direction"]["pull"]

    # ---

    def _PZA_DRV_DIO_set_direction_pull(self, v):
        """ set the pull direction
        -Args
        value : value to be set : up, down or open
        """
        self.__fakes["direction"]["pull"] = v

    # ---

    def _PZA_DRV_DIO_get_state_active(self):
        """ get the active state
        """
        return self.__fakes["state"]["active"]

    # ---

    def _PZA_DRV_DIO_set_state_active(self,v):
        """ get the active state
        -Args
        value : value to be set : True or False
        """
        self.__fakes["state"]["active"] = v

    # ---

    def _PZA_DRV_DIO_get_state_activeLow(self):
        """ get the active low state
        """
        return self.__fakes["state"]["active_low"]

    # ---

    def _PZA_DRV_DIO_set_state_activeLow(self,v):
        """
        """
        self.__fakes["state"]["active_low"] = v


