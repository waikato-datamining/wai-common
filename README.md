# wai-common
Python library with common functionality for other Waikato projects.

## Sub-modules

### memoise
Provides memoisation of function calls, so that long-running functions can restore
their results from disk instead of repeated calling.

Usage:
```python
from wai.common import memoise

memo_path: str = "./memo_fib/"

def memo_fib(a: int) -> int:
    if a == 0 or a == 1:
        return 1
    else:
        return memoise(memo_fib, a - 1, path=memo_path) + memoise(memo_fib, a - 2, path=memo_path)

memoise(memo_fib, 100, path=memo_path)
```

### switch
The switch module provides a switch/case-like pattern for operating with enumerate
values.

Usage:
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

