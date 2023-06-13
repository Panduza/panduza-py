*** Settings ***
Documentation        Multiple test to see the behaviour on the long run

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config

*** Test Cases ***

Scan interfaces of the platform multiple times
    FOR    ${robot}    IN RANGE     20
        ${INTERFACES}     Panduza Scan Server    localhost    1883
        Log    ${INTERFACES}
    END


