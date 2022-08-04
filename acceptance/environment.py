import os
import logging
from behave import *

from steps.xdocz_helpers import AttachTextLog

from fixtures.client import client
from fixtures.interface import interface_io, interface_file

from actions.platform import platform_start, platform_stop

###############################################################################
###############################################################################

ACTION_PLATFORM_START="action.platform_start."

def before_tag(context, tag):
    """Execute before each tag
    """    
    #
    # Process fixture tags
    #
    if tag.startswith("fixture.interface.io"):
        name = tag.replace("fixture.interface.io.", "")
        use_fixture(interface_io, context, name=name)
    elif tag.startswith("fixture.interface.file"):
        name = tag.replace("fixture.interface.file.", "")
        use_fixture(interface_file, context, name=name)
    elif tag.startswith("fixture.client"):
        name = tag.replace("fixture.client.", "")
        use_fixture(client, context, name=name)
    #
    # Process action tags
    #
    elif tag.startswith(ACTION_PLATFORM_START):
        treefile = tag.replace(ACTION_PLATFORM_START, "")
        platform_start(context, treefile)


###############################################################################
###############################################################################

def before_all(context):
    """Function executed before anything else
    """
    # Make sure that the directory of the acceptance report exists
    os.makedirs('acceptance/report', exist_ok=True)

    # Enable logging
    # logging.basicConfig(level=logging.DEBUG)

###############################################################################
###############################################################################

def after_all(context):
    """After all tests
    """
    # Stop running platform
    platform_stop(context)
    
    
        