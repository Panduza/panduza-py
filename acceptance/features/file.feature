@action.platform_start.io_tree.json
Feature: API File

    Panduza provides a way to transfert small files

    Rule: API File must be able to transfert the file content

        Two topics are defined to this purpose:

        | Suffix                                | QOS | Retain |
        |:--------------------------------------|:---:|:------:|
        | {INTERFACE_PREFIX}/atts/content       | 0   | true   |
        | {INTERFACE_PREFIX}/cmds/content/set   | 0   | false  |

        The payload of those topics must be a json payload:

        | Key       | Type   | Description                       |
        |:-------- :|:------:|:---------------------------------:|
        | content   | string |    |

        ```json
            {
                "content": ""
            }
        ```



