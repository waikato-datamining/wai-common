# wai-common
Python library with common functionality for other Waikato projects.

## Sub-modules

### switch
The switch module provides a switch/case-like pattern for operating with enumerate
values. See the below code-block for usage options.

```python
from wai.common import switch, case, default, break_

x: MyEnum = ...

with switch(x):
    # Standard case-block
    if case(MyEnum.ENUM_1):
        ...
        break_()
        
    # Case-block with fall-through
    if case(MyEnum.ENUM_2):
        ...
    if case(MyEnum.ENUM_3):
        ...
        break_()
        
    # Multi-case
    if case(MyEnum.ENUM_4, MyEnum.ENUM_5):
        ...
        break_()
        
    # Default block (only executes if no other case matched)
    if default():
        ...
```