from behave import *
from panduza import BooleanAttribute

@given('the boolean attribute rw {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is BooleanAttribute)
    context.boolean_att_rw = att

@given('the boolean attribute wo {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is BooleanAttribute)
    context.boolean_att_wo = att

@given('the boolean attribute ro {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is BooleanAttribute)
    context.boolean_att_ro = att

use_step_matcher("re")
@when('I set rw boolean to (true|false)')
def step_when(context, value):
    value = True if value == "true" else False
    context.boolean_att_rw.set(value)

@when('I set wo boolean to (true|false)')
def step_when(context, value):
    value = True if value == "true" else False
    context.boolean_att_wo.set(value)

@then('the rw boolean value is (true|false)')
def step_then(context, value):
    value = True if value == "true" else False
    context.boolean_att_rw.wait_for_value(value=value)

@then('the ro boolean value is (true|false)')
def step_then(context, value):
    value = True if value == "true" else False
    context.boolean_att_ro.wait_for_value(value=value)
