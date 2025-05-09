import logging
from behave import *
from panduza import Reactor
import time

@given('a reactor connected on a test platform')
def step_given(context):
    reactor = Reactor()
    reactor.start()
    context.r = reactor

    context.platform_status = context.r.new_status_attribute()
    context.platform_status.wait_for_all_instances_to_be_running()

    context.platform_notifications = context.r.new_notification_attribute()

# ---

@given('a reactor trying to connect to an invalid platform')
def step_impl(context):
    try:
        reactor = Reactor(addr="invalid")
        reactor.start()
    except Exception as e:
        context.connection_error = True

# ---

@then('the status attribute must indicate an error for one instance')
def step_then(context):
    context.platform_status.wait_for_at_least_one_instance_to_be_not_running(10)
    context.platform_status.wait_for_all_instances_to_be_running(20)
    
# ---

@then('the status attribute must indicate running for all instances')
def step_then(context):
    context.platform_status.wait_for_all_instances_to_be_running()

# ---

@then('the notification attribute must indicate no alert')
def step_then(context):
    context.platform_notifications.pop_all()

# ---

@then('the notification attribute must indicate an alert for this instance')
def step_then(context):
    time.sleep(2)
    notifications = context.platform_notifications.pop_all()
    assert(notifications.has_alert())

