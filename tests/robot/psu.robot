*** Settings ***
Documentation       Test of the Power Supply API

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config

*** Test Cases ***

Test Fake Power Supply
    Interface Psu Basic Controls    fake_psu_0
    Interface Psu Basic Controls    fake_psu_1

