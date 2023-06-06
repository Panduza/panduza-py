from ....meta_drivers.dio import MetaDriverDio

class DriverFakeDio(MetaDriverDio):

    # =============================================================================
    # FROM MetaDriverDio

    def _PZA_DRV_DIO_config(self):
        return {
            "name": "panduza.fake.dio",
            "description": "Virtual DIO"
        }

    # ---

    def _PZA_DRV_DIO_get_direction_value(self):
        """From MetaDriverDio
        """
        return 'in'

    # ---

    def _PZA_DRV_DIO_set_direction_value(self, value):
        """ set value of direction value

        -  Args
            value : value to be set : in or out
        """
        pass

    # ---

    def _PZA_DRV_DIO_get_direction_pull(self):
        """ get direction pull
        """
        return 'open'

    # ---

    def _PZA_DRV_DIO_set_direction_pull(self, v):
        """ set the pull direction
        -Args
        value : value to be set : up, down or open
        """
        pass

    # ---

    def _PZA_DRV_DIO_get_state_active(self):
        """ get the active state
        """
        return True

    # ---

    def _PZA_DRV_DIO_set_state_active(self,v):
        """ get the active state
        -Args
        value : value to be set : True or False
        """
        pass

    # ---

    def _PZA_DRV_DIO_get_state_activeLow(self):
        """ get the active low state
        """
        return False

    # ---

    def _PZA_DRV_DIO_set_state_activeLow(self,v):
        """
        """
        pass
