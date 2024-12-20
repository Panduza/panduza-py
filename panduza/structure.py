



class Structure:
    
    def __init__(self) -> None:
        self.pza_structure = {}
    
    def update(self, structure):
        self.pza_structure = structure
        print(self.pza_structure)

    

    def __find_attribute_in(self, name, instance_data):
        print("--")
        print(f"Searching in: {instance_data.get('attributes', {}).keys()} for '{name}'")

        attributes = instance_data.get("attributes")
        # print(attributes)
        print(attributes.keys())
        if name in attributes.keys():
            requested_data = attributes.get(name)
            return (name, requested_data)
        else:
            classes = instance_data.get("classes")
            for c_name, c_data in classes.items():
                found = self.__find_attribute_in(name, c_data)
                if found != None:
                    return (f"{c_name}/{found[0]}" , found[1])
        
        return None



    def find_attribute(self, name, instance=None):
        print(f"Searching for attribute '{name}' in instance '{instance}'...")

        instances = self.pza_structure.get("driver_instances")
        if not instances:
            print("No driver instances found!")
            return None

        for i_name, i_data in instances.items():
            print("--")
            print(i_data)
            found = self.__find_attribute_in(name, i_data)
            if found:
                return (f"pza/{i_name}/{found[0]}" , found[1])


        return None
    
