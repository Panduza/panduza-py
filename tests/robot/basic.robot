*** Settings ***
Documentation       Test of the Power Supply API

Resource            ../rsc/fake_bench.resource



*** Test Cases ***

Scan interfaces of the platform
    ${INTERFACES}     Panduza Scan Server    localhost    1883
    Log    ${INTERFACES}
