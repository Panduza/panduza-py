import logging
import os
import time
import base64
from behave import *
from hamcrest import assert_that, equal_to
from xdocz_helpers import AttachTextLog, PathToRsc
from panduza import Core, Client, EnsureError

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@Step('file interface "{interface_name}" initialized with alias "{interface_alias}"')
def step(context, interface_name, interface_alias):
    context.interfaces["file"][interface_name].init(alias=interface_alias)

###############################################################################
###############################################################################

@Step(u'file interface "{interface_name}" is set with content from file "{rsc_name}"')
def step(context, interface_name, rsc_name):
    filepath=PathToRsc(rsc_name)
    try:
        context.interfaces["file"][interface_name].content.set_from_file(filepath, ensure=True)
        context.ensure_error_occured = False
    except EnsureError as e:
        context.ensure_error_occured = True

###############################################################################
###############################################################################

@Step(u'atts/content data of the file interface "{interface_name}" is filled with file "{rsc_name}" content encoded in base64')
def step(context, interface_name, rsc_name):
    data = context.interfaces["file"][interface_name].content.get_data()
    filepath=PathToRsc(rsc_name)
    encoded = base64.b64encode(open(filepath, "rb").read()).decode('ascii')
    assert_that(data, equal_to(encoded))

###############################################################################
###############################################################################

@Step(u'atts/content mime of the file interface "{interface_name}" is filled "{mime_str}"')
def step(context, interface_name, mime_str):
    mime = context.interfaces["file"][interface_name].content.get_mime()
    assert_that(mime, equal_to(mime_str))

###############################################################################
###############################################################################

@Step(u'an ensure exception must have occured')
def step(context):
    assert_that(context.ensure_error_occured, equal_to(True))

