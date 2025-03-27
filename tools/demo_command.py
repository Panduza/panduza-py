import time
from panduza import Reactor


# Initialize the reactor
r = Reactor("localhost", 1883)
r.start()


# 
def value_callback(val):
    print(f"CLASS_NEW -> {val}")
CLASS_NEW = r.attribute_from_name("C1/registers/1")
CLASS_NEW.set_user_callback(value_callback)


# Conan 1, command attribute
c1_command = r.attribute_from_name("C1/command")

for i in range(50):
    c1_command.set_write_command(1, i)
    c1_command.set_read_command(1, 1)
    time.sleep(1)


time.sleep(5)
