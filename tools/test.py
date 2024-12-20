import time
from panduza import Reactor


print("pok")

# Initialize the reactor
r = Reactor("localhost", 1883)

r.start()

# Let the reactor connect and retrieve the structure
time.sleep(1)

# Specify the attribute to access
attribute_path = "json_wo"
instance_name = "json"

# Find the attribute in the structure
att_data = r.pza_structure.find_attribute(attribute_path, instance_name)
print("Attribute Data:", att_data)

json_payload = {
    "test": 42,
    "value": "example",
    "nested": {
        "key": "value"
    }
}

# Ensure the attribute exists
if att_data:
    topic, metadata = att_data
    print("Creating attribute object for topic:", topic)

    # Create an attribute object from the topic
    attribute = r.attribute_from_name(attribute_path, instance_name)

    # Set the value
    attribute.set(json_payload)
else:
    print("Attribute not found.")

# Keep the script running to observe any asynchronous behavior
time.sleep(1)
