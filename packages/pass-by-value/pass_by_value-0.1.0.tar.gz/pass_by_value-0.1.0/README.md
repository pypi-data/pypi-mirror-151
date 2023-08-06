# Pass By Value

Passing by value in Python function arguments.
## Overview

Python generally implements so called pass by object reference, that is to say, everything in Python is an object and within a function call arguments are mere references to those objects in memory. This is dangerous, because you can modify things without knowing you did. This library allows us to circumvent this behaviour in a simple decorator.

## Usage

```python

from pass_by_value import pass_by_value

@pass_by_value
def modify_list(lst):
    lst[0] = 'a'

original_list = [1,2,3,4,5]

modified_list = modify_list(original_list)

original_list # [1,2,3,4,5]

modified_list # ['a',2,3,4,5]

```

## Notes

- This library is currently very minimal and relies on `deepcopy` to copy different structures before passing them to functions
- Keep in mind that if you are passing a value you are necessarily passing a copy, so if you pass big objects/structures by value you might run out of memory
