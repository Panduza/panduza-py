import threading


class Attribute:
    
    def __init__(self, reactor, topic, mode, settings):
        
        self.value = None
        self.client = reactor.client

        self.mode = mode
        self.settings = settings

        self.topic = topic
        self.topic_att = f"{topic}/att"
        self.topic_cmd = f"{topic}/cmd"
        
        self.client.subscribe(self.topic_att)
        
        self._update_event = threading.Event()
    
    def onMessage(self, data):
        print("onMessage !!!!!!!!!!", data)
        self.value = data
        #     for (var cb in onChangeCallbacks) {
        #       await cb!(data);
        #     }
        #   }
        # Thread trigger
        self._update_event.set()



    def wait_for_first_value(self):
        if self.value == None:
            self._update_event.wait(1)


    def get(self):
        return self.value

    def set(self, value):
        self.client.publish(self.topic_cmd, value, qos=0)


