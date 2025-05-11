from enum import Enum
from dataclasses import dataclass
from typing import Any

class InstanceState(Enum):
    Booting = "Booting"
    Connecting = "Connecting"
    Initializating = "Initializating"
    Running = "Running"
    Warning = "Warning"
    Error = "Error"
    Cleaning = "Cleaning"
    Stopping = "Stopping"
    Undefined = "Undefined"

    def __str__(self) -> str:
        return self.value

    def to_u16(self) -> int:
        mapping = {
            InstanceState.Undefined: 0,
            InstanceState.Booting: 1,
            InstanceState.Connecting: 2,
            InstanceState.Initializating: 3,
            InstanceState.Running: 4,
            InstanceState.Warning: 5,
            InstanceState.Error: 6,
            InstanceState.Cleaning: 7,
            InstanceState.Stopping: 8,
        }
        return mapping[self]

# Example usage:
if __name__ == "__main__":
    state = InstanceState.Booting
    print(str(state))  # Output: Booting
    print(state.to_u16())  # Output: 1

    