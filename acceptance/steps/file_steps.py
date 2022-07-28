import logging
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

@Step('file interface "{interface_name}" initialized with alias "{interface_alias}"')
def step(context, interface_name, interface_alias):
    context.interfaces["file"][interface_name].init(alias=interface_alias)

###############################################################################
###############################################################################

@Step(u'file interface "{interface_name}" is set with content from file "{rsc_name}"')
def step(context, interface_name, rsc_name):
    filepath=PathToRsc(rsc_name)
    AttachTextLog(context, f'Loaded filepath "{filepath}"')
    context.interfaces["file"][interface_name].content.set_from_file(filepath)

###############################################################################
###############################################################################

@Step(u'atts/content of file interface "{interface_name}" is filled with file "{rsc_name}" content encoded in base64')
def step(context, interface_name, rsc_name):
    # filepath=PathToRsc(rsc_name)
    pass
    # logging.debug(filepath)
    # context.interfaces["file"][interface_name].content.set_from_file(filepath)

###############################################################################
###############################################################################


