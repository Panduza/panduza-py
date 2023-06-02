*** Settings ***
Documentation       Test of the Power Supply API

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config

*** Test Cases ***

Test polling cycles
    Set Power Supply Voltage Polling Cycle    psu_1    2

Test polling cycles max
    Set Power Supply Voltage Polling Cycle    psu_1    0

Test polling cycles disbale
    Set Power Supply Voltage Polling Cycle    psu_1    -1

Enable settings
    Turn Power Supply Ovp Setting    psu_1    True
    Turn Power Supply Ocp Setting    psu_1    True

Test Fake Power Supply
    Interface Psu Basic Controls    psu_1

