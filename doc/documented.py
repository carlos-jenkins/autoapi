# -*- coding: utf-8 -*-
"""
This is my module brief line.

This is a more complete paragraph documenting my module.

- A list item.
- Another list item.

This section can use any reST syntax.
"""

A_CONSTANT = 1000
"""This is an important constant."""


def a_function(my_arg, another):
    """
    This is the brief description of my function.

    This is a more complete example of my function. It can include doctest,
    code blocks or any other reST structure.

    >>> a_function(10, [MyClass('a'), MyClass('b')])
    20

    :param int my_arg: The first argument of the function. Just a number.
    :param another: The other argument of the important function.
    :type another: A list of :class:`MyClass`
    :rtype: int
    :return: The length of the second argument times the first argument.
    """
    return my_arg * len(another)


class MyClass(object):
    """
    This is the brief of my main class.

    A more general description of what the class does.

    :param int param1: The first parameter of my class.
    :param param2: The second one.
    :type param2: int or float
    :var my_attribute: Just an instance attribute.
    :raises TypeError: if param2 is not None.
    """

    class_attribute = 625
    """This is a class attribute."""

    def __init__(self, param1, param2=None):
        self.param1 = param1
        if param2 is not None:
            raise TypeError()
        self.param2 = param2
        self.my_attribute = 100

    def my_method(self, param1, param2):
        """
        The brief of this method.

        This method does many many important things.

        :param int param1: A parameter.
        :param list param2: Another parameter.
        :rtype: list of int
        :return: A list of the first parameter as long a the length of the
         second parameter.
        """
        return [param1] * len(param2)


class AnotherClass(MyClass):
    """
    This another class.

    Check the nice inheritance diagram. See :class:`MyClass`.
    """


class MyException(Exception):
    """
    This is my custom exception.

    This is a more complete description of what my exception does. Again, you
    can be as verbose as you want here.
    """


__all__ = [
    'A_CONSTANT',
    'a_function',
    'MyClass',
    'AnotherClass',
    'MyException'
]
