TinkerTest
==========
Inline testing/validation in python 3, based on this wonderful blog post: https://tinkering.xyz/abusing-type-annotations/

## What is this?
TinkerTest aims to simplify data validation checking in both unit tests and production environments. In order to do this
conveniently, TinkerTest ~~abuses~~ makes use of the fact that python type annotations can be any arbitrary python 
expression. Using this fact allows us to inject validation logic into your scripts which simply evaluate your type 
annotations.

## Helpful Hint
Starting from python 3.7, the `annotations` future import exists. This may be helpful for you, as its lazy evaluation
should prevent some common mistakes in using this library.

## Trivial Example
```python
# my_script.py
from tinkertest import inject_into_type

class MyClass:
    my_field: 'my_field < 0'  # This field only accepts values < 0
    my_str_field: str  # This field only accepts strings
    
    def __init__(self, my_field, my_str_field):
        self.my_field = my_field
        self.my_str_field = my_str_field
        
    # This function only accepts a non-None argument and should always return 1
    def some_func(self, input_val: 'input_val is not None') -> 'returned == 1':  # 'returned' is a magic variable for use in return annotations
        ...
        
inject_into_type(MyClass)  # Wires all the injections, now any calls will be validated!
```
