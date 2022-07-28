from behave import fixture

from panduza import Io
from panduza import File

###############################################################################

@fixture
def interface_io(context, name):
    # -- SETUP-FIXTURE PART:
    if "interfaces" not in context:
        context.interfaces = dict()
    if "io" not in context.interfaces:
        context.interfaces["io"] = dict()
    context.interfaces["io"][name] = Io()

    # -- READY FOR THE STEP --
    yield context.interfaces["io"][name]

    # -- CLEANUP-FIXTURE PART:

###############################################################################

@fixture
def interface_file(context, name):
    # -- SETUP-FIXTURE PART:
    if "interfaces" not in context:
        context.interfaces = dict()
    if "file" not in context.interfaces:
        context.interfaces["file"] = dict()
    context.interfaces["file"][name] = File()

    # -- READY FOR THE STEP --
    yield context.interfaces["file"][name]

    # -- CLEANUP-FIXTURE PART:

###############################################################################

