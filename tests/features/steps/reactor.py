from behave import *
from panduza import Reactor
import time



@then('the reactor returned an error')
def step_then(context):
    assert context.connection_error is True

@then('the reactor is successfully connected to the platform')
def step_then(context):
    assert context.r is not None

@given('an attribute name {string}')
def step_given(context, string):
    context.att_name = string.strip('"')

@when('the reactor find function is called with the previously given attribute name')
def step_when(context):
    try:
        context.att = context.r.find(context.att_name)
        context.find_result = True
    except Exception as e:
        context.find_result = False
        context.att = None

@then('the reactor must return a null value')
def step_then(context):
    assert context.find_result is False

@then('the reactor must return a success')
def step_then(context):
    assert context.find_result is True