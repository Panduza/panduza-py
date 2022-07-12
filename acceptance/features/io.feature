@action.platform_start.io_tree.json
Feature: API Io

    Panduza provides a way to control simple input/output signals

    Rule: API Io must be able to drive io direction

        Two topics are defined for this purpose:

        | Suffix                                | QOS | Retain |
        |:-------------------------------------:|:---:|:------:|
        | {INTERFACE_PREFIX}/atts/direction     | 0   | true   |
        | {INTERFACE_PREFIX}/cmds/direction/set | 0   | false  |

        The payload of those topics must be a json payload:

        | Key       | Type   | Description                       |
        |:-------- :|:------:|:---------------------------------:|
        | direction | string | direction of the io 'in' or 'out' |

        ```json
            {
                "direction": "in"
            }
        ```


        @fixture.interface.io.test
        Scenario: Io direction must be configurable
            Given core aliases loaded with file "io_alias.json"
            And  io interface "test" initialized with alias "io_test"
            When io interface "test" direction is set to "out"
            Then io interface "test" direction is "out"
            When io interface "test" direction is set to "in"
            Then io interface "test" direction is "in"

        @fixture.interface.io.test
        Scenario: Io value must be configurable
            Given core aliases loaded with file "io_alias.json"
            And  io interface "test" initialized with alias "io_test"
            When io interface "test" direction is set to "out"
            Then io interface "test" direction is "out"
            When io interface "test" value is set to "0"
            Then io interface "test" value is "0"

# -----------------------------------------------------------------------------

    @fixture.interface.io.in
    @fixture.interface.io.out
    Scenario: Io value must support operation set and get through 2 interfaces in loopback
        Given core aliases loaded with file "io_alias.json"
        And  io interface "in" initialized with alias "io_in"
        And  io interface "out" initialized with alias "io_out"
        When io interface "in" direction is set to "in"
        And  io interface "out" direction is set to "out"
        When io interface "out" value is set to "1"
        Then io interface "in" value is "1"
        When io interface "out" value is set to "0"
        Then io interface "in" value is "0"

# -----------------------------------------------------------------------------

# @action.platform_close
