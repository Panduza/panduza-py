*** Settings ***
Documentation        Basic test for panduza interfaces

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config


*** Test Cases ***

Scan interfaces of the platform
    ${INTERFACES}     Panduza Scan Server    localhost    1883
    Log    ${INTERFACES}

Test fake dio interfaces
    Test Basic Access Of Dio Interface     fake_dio_0
