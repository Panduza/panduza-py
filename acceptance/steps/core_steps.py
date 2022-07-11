import os
import time
import logging
from behave import *
from panduza import Core
from xdocz_helpers import PathToRsc

###############################################################################
###############################################################################

# Required to parse arguments in steps, for example "{thing}"
use_step_matcher("parse")

###############################################################################
###############################################################################

@Step('aliases "{file}" are loaded into the core')
def step(context, file):
    # Core.LoadAliases(json_filepath=PathToRsc(file))
    pass

###############################################################################
###############################################################################

@Step(u'each connection and aliases are declared')
def step(context):
    # Just get the current path
    # context.cwd = os.getcwd()
    pass
