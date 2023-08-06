# DataclassModule

dataclass + nn.Module

## Usage 

```python
from dataclassmodule import DataclassModule

class ExampleModule(DataclassModule):
    x: int
    
    def __post_init__(self):
        self.layer = nn.Linear(2, 2)
```