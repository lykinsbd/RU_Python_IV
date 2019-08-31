#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_subprocess` -- subprocess module
============================================

LAB subprocess Learning Objective: Familiarization with subprocess

::

 a. Use the subprocess run function to run "ls -l" and print the output.

 b. Do the same as a), but don't print anything to the screen.

 c. Do the same as a), but run the command "/bogus/command". What happens?

 d. Use subprocess run function to run "du -h" and output stdout to a pipe. Read the pipe
    and print the output.

 e. Create a new function commander() which takes in a list of commands to execute
    (as strings) on the arg list, then runs them sequentially printing stdout.

"""


import shlex
import subprocess


def main() -> None:
    """
    do stuff and things
    :return:
    """

    # a. Use the subprocess run function to run "ls -l" and print the output.
    print("Task A:")
    subprocess.run(["ls", "-l"])

    # b. Do the same as a), but don't print anything to the screen.
    print("\nTask B:")
    subprocess.run(["ls", "-l"], stdout=subprocess.DEVNULL)

    # c. Do the same as a), but run the command "/bogus/command". What happens?
    print("\nTask C:")
    try:
        subprocess.run(["/bogus/command"])
    except FileNotFoundError:
        print("Y u give me stupid things?")

    # d. Use subprocess run function to run "du -h" and output stdout to a pipe. Read the pipe and print the output.
    print("\nTask D:")
    output = subprocess.run(["du", "-h"], stdout=subprocess.PIPE)
    print(output.stdout.decode())

    # e.  Create a new function commander() which takes in a list of commands to execute (as strings) on the arg list,
    # then runs them sequentially printing stdout.
    print("\nTask E:")
    commander(["ls -alF", "du -h"])


def commander(commands: list) -> None:
    """
    Execute a list of commands, print the output to stdout
    :param commands:
    :return:
    """

    for command in commands:
        output = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{ command } - Output:\n{ output.stdout.decode() }")


if __name__ == '__main__':
    main()
