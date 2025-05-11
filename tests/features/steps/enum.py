from behave import *
from panduza import Reactor
import time

from panduza import EnumAttribute

@given('the enum attribute rw {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is EnumAttribute)
    context.enum_att_rw = att

@given('the enum attribute wo {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is EnumAttribute)
    context.enum_att_wo = att

@given('the enum attribute ro {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is EnumAttribute)
    context.enum_att_ro = att

@when('I set rw enum to {string}')
def step_when(context, string):
    string = string.strip('"')
    context.enum_att_rw.set(string)

@when('I set wo enum to {string}')
def step_when(context, string):
    string = string.strip('"')
    context.enum_att_wo.set(string)

@then('the rw enum value is {string}')
def step_then(context, string):
    string = string.strip('"')
    context.enum_att_rw.wait_for_value(value=string)

@then('the ro enum value is {string}')
def step_then(context, string):
    string = string.strip('"')
    context.enum_att_ro.wait_for_value(value=string)
