*** Settings ***
Documentation        Basic tests for panduza interfaces

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config

*** Test Cases ***

Scan interfaces of the platform
    ${INTERFACES}     Panduza Scan Server    localhost    1883
    Log    ${INTERFACES}

Test Fake DIO interfaces
    Test Basic Access Of Dio Interface         fake_dio_0

Test Fake AmpereMeter interfaces
    Test Basic Access Of Ammeter Interface        fake_ammeter_0

Test Fake VoltMeter interfaces
    Test Basic Access Of VoltMeter Interface        fake_voltmeter_0

Test Fake BPS interfaces
    Interface Bps Basic Controls    fake_bps_0
    Interface Bps Basic Controls    fake_bps_1

Test Fake Relay interfaces
    Test Basic Access Of Relay Interface           fake_relay_0



