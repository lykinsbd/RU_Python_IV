#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_args` -- Arguing with the functions
=========================================

LAB_ARGS Learning Objective: Learn to modify, receive, and work with arguments to function.
::

 a. Create a function that accepts any number of positional arguments and
    keyword arguments and prints the argument values out to the screen.

 b. Create a function that takes in any number of positional arguments, turns
    those arguments into keyword arguments using "arg#" for the keyword names,
    and calls the print function you wrote in a.

 c. Write a validation function that takes in a variable number of positional
    arguments.  Validate that all the arguments passed in are integers and are
    greater than 0.  If the arguments validate, call the print function, if an
    argument doesn't validate raise a ValueError.

"""


def main():
    """
    do some arguing
    :return:
    """

    print("======== [ Print some args and kwargs! ] ========\n")
    any_args(1, 2, 3, a=1, b=2, c=3)

    print("\n======== [ Passing some args to args_to_kwargs() and mutating and printing them! ] ========\n")
    args_to_kwargs(1, 2, 3, 4, 5)

    print("\n======== [ Validating if some args are ints and greater than 0 ] ========\n")
    try:
        validator(1, 2, -1)
    except ValueError as e:
        print(e)


def any_args(*args, **kwargs):
    """
    take in any number of positional/keyword args and prints them
    :param args:
    :param kwargs:
    :return:
    """

    print("Printing args:")
    if not args == ():
        for arg in args:
            print(f"Argument: {arg}")
    else:
        print("No args provided")

    print("Printing kwargs:")
    if not kwargs == {}:
        for kwarg in kwargs:
            print(f"Keyword Argument: {kwarg} = {kwargs[kwarg]}")
    else:
        print("No kwargs provided")


def args_to_kwargs(*args):
    """
    Take any args and turn em into kwargs like arg0 = arg and pass them to any_args
    :param args:
    :return:
    """

    print("Mutating our args to kwargs.")
    mah_kwargs = {}
    counter = 0
    for arg in args:
        kwarg = "arg" + str(counter)
        mah_kwargs[kwarg] = arg
        counter += 1

    print("Passing our kwargs to any_args()")
    any_args(**mah_kwargs)


def validator(*args):
    """
    Validates that arguments are integers and are greater than 0

    Prints them if they do.

    Will raise ValueError if they don't
    :param args:
    :return:
    """

    if not args == ():
        for arg in args:
            if not isinstance(arg, int):
                raise ValueError(f"{arg} is not an int!")

            if arg <= 0:
                raise ValueError(f"{arg} is not greater than zero!")

            print(f"Argument: {arg}")
    else:
        print("No args provided")
        return


if __name__ == '__main__':
    main()
