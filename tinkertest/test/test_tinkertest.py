import traceback
from warnings import warn

from tinkertest import tinkertest as tt


class MyClass:

    my_field: 'my_field < 5'

    my_field_2: 'int'

    def __init__(self, my_field, my_field_2):
        self.my_field = my_field
        self.my_field_2 = my_field_2


def report_assertion(callable):
    try:
        callable()
    except AssertionError as e:
        warn("Assertion caught!")
        traceback.print_exception(AssertionError, e, e.__traceback__)


def main():
    print("No error")
    report_assertion(lambda: MyClass(6, 1))
    tt.inject_assertions(MyClass)
    print("No error")
    report_assertion(lambda: MyClass(3, 1))
    print("Error...")
    report_assertion(lambda: MyClass(6, 1))
    print("Error...")
    report_assertion(lambda: MyClass(1, '1'))


if __name__ == '__main__':
    main()
