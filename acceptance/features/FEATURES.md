# Features

This documentation describes Panduza Features.

## Panduza MQTT levels

Panduza levels are defined as follow

```
INTERFACE_PREFIX: pza/[machine]/[driver]/[interface]
```

- **pza**       : to tag all the topics matching the Panduza specification
- **machine**   : defines the host on which the driver is located. It should be the name of the physical device that support the driver.
- **driver**    : defines the name of the driver that support this interface. It should be the name of the process running the driver.
- **interface** : defines the interface name.

```
{INTERFACE_PREFIX}/[specifier]/[attribut]
```

- **specifier** : [atts|cmds|info]
- **attribut**  : defines the specific element of the interface to monitor.

