from panduza.instance_state import InstanceState
from ..attribute import Attribute
from ..fbs import Status
import time

class StatusAttribute(Attribute):
    """
    Attribute for sending boolean values (True or False).
    Ensures that only valid booleans are sent.
    """
   
    # ---

    def __init__(self, reactor, topic, mode, settings=None):
        super().__init__(reactor, topic, mode, settings)
    
    # ---

    def on_att_message(self, data):
        """
        Callback for handling incoming messages.
        - Updates the value and triggers the update event.
        """
        obj = Status.Status.GetRootAsStatus(data, 0)
        # print(f"!!!!! $$$$$$ DATA")
        self.value = obj
        super().on_message_top(obj)
    
    # ---

    def all_instances_are_running(self):
        """
        Check if all instances are running.
        - Returns True if all instances are running, False otherwise.
        """
        
        # print(f"!!!all_instances_are_running {self.value} !!!!")

        # Check if value is initialized
        if not hasattr(self, 'value') or self.value is None:
            print("Value is not initialized.")
            return False
        
        # Get the number of instances
        instances_count = self.value.InstancesLength()
        
        # If there are no instances, consider it as not running
        if instances_count == 0:
            print("No instances found.")
            return False
        
        # Check each instance status
        for i in range(instances_count):
            instance = self.value.Instances(i)
            
            state = instance.State()
            
            # print(f"Instance {i} state: {state}")
            
            # Check if this instance has a status other than InstanceState.Running
            if state != InstanceState.Running.to_u16():
                # print(f"FALSE")
                return False
        
        # If we've checked all instances and none failed the test, all are running
        # print("TRUE")
        return True
    
    
    def wait_for_all_instances_to_be_running(
        self,
        timeout_duration: float = 5.0):
        """
        Wait for all instances to be running.
        - Blocks until all instances are running or the timeout is reached.
        """
        start_time = time.time()
        while not self.all_instances_are_running():
            if time.time() - start_time > timeout_duration:
                raise TimeoutError("Timeout reached while waiting for all instances to be running.")
            time.sleep(0.5)  # Sleep briefly to avoid busy-waiting
    


    def at_least_one_instance_is_not_running(self):

        # Check if value is initialized
        if not hasattr(self, 'value') or self.value is None:
            print("Value is not initialized.")
            return False
        
        # Get the number of instances
        instances_count = self.value.InstancesLength()
        
        # If there are no instances, consider it as not running
        if instances_count == 0:
            print("No instances found.")
            return False
        
        # Check each instance status
        for i in range(instances_count):
            instance = self.value.Instances(i)
            
            state = instance.State()
            
            # Check if this instance has a status other than InstanceState.Running
            if state != InstanceState.Running.to_u16():
                # print(f"FALSE")
                return True
        
        # If we've checked all instances and none failed the test, all are running
        # print("TRUE")
        return False

    def wait_for_at_least_one_instance_to_be_not_running(
        self,
        timeout_duration: float = 5.0):
        """
        Wait for at least one instance to be not running.
        - Blocks until at least one instance is not running or the timeout is reached.
        """
        start_time = time.time()
        while not self.at_least_one_instance_is_not_running():
            if time.time() - start_time > timeout_duration:
                raise TimeoutError("Timeout reached while waiting for at least one instance to be not running.")
            time.sleep(0.5)

    # def set(self, value):
    #     """
    #     Set a boolean value.
    #     - Ensures the value is either True or False.
    #     - Sends the boolean value directly (or as a string if required).
    #     """
    #     # Mode check
    #     if self.mode == "RO":
    #         raise Exception("Cannot 'set' a Read-Only attribute")
        
    #     # Validate that the input is a boolean
    #     if not isinstance(value, bool):
    #         raise ValueError(f"Invalid value for StatusAttribute. Expected a boolean, got: {type(value)}")

    #     # Convert boolean to its string equivalent 'true' or 'false' if necessary
    #     boolean_value = "true" if value else "false"

    #     # Use the parent class's set method to send the raw value
    #     super().set(boolean_value)
    #     self.logger.debug(f"Set value to {boolean_value}")
        
    #     # Make sur change is ok
    #     if self.mode == "RW":
    #         super().wait_for_value(value)
    
