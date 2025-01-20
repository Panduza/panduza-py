import time
from panduza import Reactor


# Initialize the reactor
r = Reactor("localhost", 1883)

r.start()


def cb(val):
    print(val)


# Find the attribute in the structure
c1_command = r.attribute_from_name("C1/command")
c1_r0 = r.attribute_from_name("C1/registers/0")

c1_r0.set_user_callback(cb)


for i in range(50):
    c1_command.set_write_command(0, i)
    c1_command.set_read_command(0, 1)


time.sleep(5)
