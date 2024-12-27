import logging
import fnmatch

class Structure:
    
    # ---

    def __init__(self) -> None:
        # Create a logger for reactor
        self.logger = logging.getLogger(__name__)

        # Structure initialized as empty
        self.pza_structure = {}

        # Structure flat
        self.pza_structure_flat = {}

    # ---

    def update(self, structure):
        # Store new sturcture
        self.pza_structure = structure

        # Reset flat structure
        self.pza_structure_flat = {}

        # Basic structure check
        instances = self.pza_structure.get("driver_instances")
        if not instances:
            self.logger.error("No driver instances found in structure!")
            return None

        # Build flat structure
        for i_name, i_data in instances.items():
            self.flatten_structure(f"pza/{i_name}", i_data)

        # debug
        # self.logger.debug(f"Structure updated: {self.pza_structure_flat.keys()}")

    # ---

    def flatten_structure(self, level, data):
        """Flatten the structure of the PZA

        Compose a flat structure of the PZA, where each attribute is stored
        with its full path in the structure.
        """
        # 
        attributes = data.get("attributes")
        for a_name, a_data in attributes.items():
            self.pza_structure_flat[f"{level}/{a_name}"] = a_data
            
        # 
        classes = data.get("classes")
        for c_name, c_data in classes.items():
            self.flatten_structure(f"{level}/{c_name}", c_data)
        
    # ---

    def find_attribute_from_xtopic(self, xtopic):
        # Debug
        self.logger.debug(f"Searching for attribute from xtopic '{xtopic}'...")

        # Check if xtopic is a full path else append a * to match any attribute
        if not xtopic.startswith("pza/"):
            xtopic = f"*{xtopic}"

        # Find attribute in flat structure
        matches = fnmatch.filter(self.pza_structure_flat.keys(), xtopic)
        self.logger.debug(f"Matches: {matches}")

        # 
        if len(matches) > 1:
            raise Exception(f"Multiple matches found for '{xtopic}'!")
        elif len(matches) == 1:
            return (matches[0], self.pza_structure_flat[matches[0]])
        else:
            raise Exception(f"Attribute '{xtopic}' not found in flat structure!")
