import os
import time
from behave import *
from hamcrest import assert_that, equal_to
from xdocz_helpers import AttachTextLog, PathToRsc
from panduza import Core, Client

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################


@Given('the client "{client_name}" initialized with test broker url:"{url}" and port:"{port}"')
def step(context, client_name, url, port):
    context.clients[client_name] = Client(url=url, port=int(port))
    AttachTextLog(
        context, f"Client created with url:'{url}' and port:'{port}'")

###############################################################################
###############################################################################


@Given('a client "{client_name}" initialized with the mqtt test broker alias:"{alias}"')
def step(context, client_name, alias):
    context.clients[client_name] = Client(broker_alias=alias)
    AttachTextLog(
        context, f"Client created with url:'{context.clients[client_name].url}' and port:'{context.clients[client_name].port}'")

###############################################################################
###############################################################################


@When('the client "{client_name}" start the connection')
def step(context, client_name):
    context.clients[client_name].connect()

###############################################################################
###############################################################################


@Then('the client "{client_name}" is connected')
def step(context, client_name):
    time.sleep(0.1)
    assert context.clients[client_name].is_connected == True

###############################################################################
###############################################################################


@When('the client "{client_name}" scan the interfaces')
def step(context, client_name):
    context.scanned_interfaces = context.clients[client_name].scan_interfaces()
    AttachTextLog(context, f"interfaces: {context.scanned_interfaces}")

###############################################################################
###############################################################################


@Then('at least a platform interface must be found')
def step(context):
    found_platform = False
    for i in context.scanned_interfaces:
        if context.scanned_interfaces[i]["type"]:
            found_platform = True
    assert found_platform == True


###############################################################################
###############################################################################

@When('the client "{client_name}" subscribe to topic "{topic}"')
def step(context, client_name, topic):

    def fff(topic, payload, context):
        context.rx_data = payload
        # print(">>>", context.rx_data, "\n")

    context.rx_data = None
    context.clients[client_name].subscribe(topic, fff, context=context)
    time.sleep(0.5)

###############################################################################
###############################################################################


@When('the client "{client_name}" send "{data}" in topic "{topic}"')
def step(context, client_name, data, topic):
    context.clients[client_name].publish(topic, data)
    AttachTextLog(context, f"data rx: {context.rx_data} vs {data}")

###############################################################################
###############################################################################


@Then('the client "{client_name}" has recieved "{data}"')
def step(context, client_name, data):
    time.sleep(0.5)
    assert context.rx_data.decode() == data

###############################################################################
###############################################################################


@When('the client "{client_name}" unsubscribe from the topic "{topic}"')
def step(context, client_name, topic):
    context.clients[client_name].unsubscribe(topic)

###############################################################################
###############################################################################

@Then('the client "{client_name}" has "{count}" listener')
def step(context, client_name, count):
    assert_that(context.clients[client_name].listeners_number(), equal_to(int(
        count)))

###############################################################################
###############################################################################

@When('the client "{client_name}" subscribe 3 callback to topic "{topic}" and unsubscribe 1')
def step(context, client_name, topic):

    def f1(topic, payload):
        pass
    def f2(topic, payload):
        pass
    def f3(topic, payload):
        pass

    context.clients[client_name].subscribe(topic, f1)
    context.clients[client_name].subscribe(topic, f2)
    context.clients[client_name].subscribe(topic, f3)
    context.clients[client_name].unsubscribe(topic, f2)
