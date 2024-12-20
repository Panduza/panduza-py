import time
from panduza import Reactor


r = Reactor("localhost", 1883)

r.start()



pp = r.attribute_from_name("voltage", None)





print("min ----", pp.min())
print("max ----", pp.max())

pp.set(4)



# # r.find_attribute("3").on_device("memory_map").into_topic()

# att = r.attribute("pza/L-8J2NLB3/memory_map/registers/3", None)


# print("pik")

time.sleep(10)

