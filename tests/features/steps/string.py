from behave import *
from panduza import Reactor
import time

from panduza import StringAttribute

@given('the string attribute rw {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is StringAttribute)
    context.string_att_rw = att

@given('the string attribute wo {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is StringAttribute)
    context.string_att_wo = att

@given('the string attribute ro {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is StringAttribute)
    context.string_att_ro = att

@when('I set rw string to {string}')
def step_when(context, string):
    string = string.strip('"')
    context.string_att_rw.set(string)

@when('I set wo string to {string}')
def step_when(context, string):
    string = string.strip('"')
    context.string_att_wo.set(string)

@then('the rw string value is {string}')
def step_then(context, string):
    string = string.strip('"')
    context.string_att_rw.wait_for_value(value=string)

@then('the ro string value is {string}')
def step_then(context, string):
    string = string.strip('"')
    context.string_att_ro.wait_for_value(value=string)
