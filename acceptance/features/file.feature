@action.platform_start.io_tree.json
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

    Rule: API File must be able to read file data

        1 topic are defined to this purpose:

        | Suffix                                | QOS | Retain |
        |:--------------------------------------|:---:|:------:|
        | {INTERFACE_PREFIX}/atts/data          | 0   | true   |

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

