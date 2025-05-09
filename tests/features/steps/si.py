from behave import *
from panduza import SiAttribute

@given('the si attribute rw {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is SiAttribute)
    context.si_att_rw = att

@given('the si attribute wo {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is SiAttribute)
    context.si_att_wo = att

@given('the si attribute ro {string}')
def step_given(context, string):
    string = string.strip('"')
    att = context.r.find(string)
    assert(type(att) is SiAttribute)
    context.si_att_ro = att

use_step_matcher("re")
@when('I set rw si to ([-+]?[0-9]*\.?[0-9]+)')
def step_when(context, value):
    value = float(value)
    context.si_att_rw.set(value)

@when('I set wo si to ([-+]?[0-9]*\.?[0-9]+)')
def step_when(context, value):
    value = float(value)
    context.si_att_wo.set(value)

@then('the rw si value is ([-+]?[0-9]*\.?[0-9]+)')
def step_then(context, value):
    value = float(value)
    context.si_att_rw.wait_for_value(value=value)

@then('the ro si value is ([-+]?[0-9]*\.?[0-9]+)')
def step_then(context, value):
    value = float(value)
    context.si_att_ro.wait_for_value(value=value)
