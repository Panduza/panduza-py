@action.platform_start.file_tree.json
Feature: API File

    Panduza provides a way to transfert small files

    Rule: API File must be able to transfert the file content

        2 topics are defined to this purpose:

        | Suffix                                | QOS | Retain |
        |:--------------------------------------|:---:|:------:|
        | {INTERFACE_PREFIX}/atts/content       | 0   | true   |
        | {INTERFACE_PREFIX}/cmds/content/set   | 0   | false  |

        The payload of those topics must be a json payload:

        | Key       | Type          | Description                            |
        |:-------- :|:-------------:|:--------------------------------------:|
        | content   | base64 string | Content of the file encoding in base64 |

        ```json
            {
                "content": "SKGKFGD ... JGBEIGDFGPD"
            }
        ```

        @fixture.interface.file.test
        Scenario: Transfert simple file
            Given core aliases loaded with file "file_alias.json"
            And   file interface "test" initialized with alias "file_test"
            # When  the file 
            

    Rule: API File must be able to read file properties

        1 topic is defined to this purpose:

        | Suffix                                | QOS | Retain |
        |:--------------------------------------|:---:|:------:|
        | {INTERFACE_PREFIX}/atts/properties    | 0   | true   |

        The payload of this topic must be a json payload:

        | Key       | Type          | Description                                   |
        |:-------- :|:-------------:|:---------------------------------------------:|
        | size      | number        | size of the file content in bytes             |
        | crc       | string        | crc32 of the file content in string format    |

        ```json
            {
                "size": 12345, "crc": "0xFFFF50"
            }
        ```

# @action.platform_close

