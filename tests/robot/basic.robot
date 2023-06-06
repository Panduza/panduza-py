*** Settings ***
Documentation       Test of the Power Supply API

Resource            ../rsc/fake_bench.resource



*** Test Cases ***

Scan interfaces of the platform
    ${INTERFACES}     Panduza Scan Server    localhost    1883
    Log    ${INTERFACES}

Test fake dio interfaces
    Test Basic Access Of Dio Interface     fake_dio_0
