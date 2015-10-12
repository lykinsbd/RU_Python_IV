#!/usr/bin/env python
#!*-* coding:utf-8 *-*

"""

:mod:`lab_pyreview` -- Python review
=========================================

LAB PyReview Learning Objective: Familiarization with argparse and parsing command line arguments.


a. Review argparse module documentation

b. Build an ArgumentParser object using the following parameters:
   description: "Patent database search engine"

c. Add support for the following arguments and argument attributes:
   -a --author last first
   -p --patent_num
   -f --filing_date

d. Run parse_args() to build arguments objects and print the Namespace

e. Construct a generator called test_db_load() that returns a random function from a list of functions.
   The list will support find_by_author(), find_by_patent_number(), and find_by_filing date()
   Test your generator with stub functions

"""

import argparse
import random

def find_by_author():
    """ Stub. """
    print "find_by_author() invoked"


def find_by_patent_number():
    """ Stub. """
    print "find_by_patent_number() invoked"


def find_by_filing_date():
    """ Stub. """
    print "find_by_filing_date() invoked"


def test_db_load():
    """ Generator to return a random function from func_set list.  """
    func_set = [ find_by_author,
                 find_by_patent_number,
                 find_by_filing_date ]
    while True:
        next_func = random.randint(0,len(func_set) - 1)
        yield func_set[next_func]


def test_rand_func_gen():
    """ Tests test_db_load generator. """
    rand_func = test_db_load()

    for run in range(10):
        rand_func.next()()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Patent database search engine')
    parser.add_argument('-a', '--author', nargs=2, dest='author_last_first',
                       help='Last name followed by first name [partial names ok]')
    parser.add_argument('-p', '--patent_num', dest='patent_num',
                       help='Patent number')
    parser.add_argument('-f', '--filing_date', dest='filing_date',
                       help='Filing date in iso8601 format')

    args = parser.parse_args()
    print "Command line arguments:"
    print vars(args)

    print "\nRandom function generator:"
    test_rand_func_gen()
