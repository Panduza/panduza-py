import time
from panduza import Reactor


# Initialize the reactor
r = Reactor("localhost", 1883)

r.start()



# Find the attribute in the structure
boolean_rw = r.attribute_from_name("boolean_rw")

boolean_ro = r.attribute_from_name("boolean_ro")


boolean_rw.set(True)
time.sleep(1)
boolean_rw.set(False)
time.sleep(1)


boolean_wo = r.attribute_from_name("boolean_wo")
boolean_wo.set(True)
time.sleep(1)
boolean_wo.set(False)
time.sleep(1)

