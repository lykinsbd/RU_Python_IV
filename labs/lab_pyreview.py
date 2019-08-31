#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

:mod:`lab_pyreview` -- Python review
=========================================

LAB PyReview Learning Objective: Review the topics from the previous courses

a. Load the data from the two dictionary files in the data directory into two
   list objects.  data/dictionary1.txt data/dictionary2.txt
   Print the number of entries in each list of words from the dictionary files.

b. Use sets in Python to merge the two lists of words with no duplications (union).
   Print the number of words in the combined list.

c. Import the random library and use one of the functions to print out five random
   words from the combined list of words.

d. Use a list comprehension to find all the words that start with the letter 'a'.
   Print the number of words that begin with the letter 'a'.

e. Create a function called wordcount() with a yield that takes the list of
   all words as an argument and yields a tuple of
   (letter, number_of_words_starting_with_that_letter) with each iteration.

"""

import random

from string import ascii_lowercase


def main() -> None:
    """
    Doin' stuff
    :return:
    """

    print("Doing some stuff with two 'Dictionaries' of words.\n")
    dictionary_1_path = "/Users/bret7530/Documents/scripts/Envs/RU_Python_IV/data/dictionary1.txt"
    dictionary_2_path = "/Users/bret7530/Documents/scripts/Envs/RU_Python_IV/data/dictionary2.txt"

    # Grab the dictionaries
    print(f"Reading in { dictionary_1_path }...")
    with open(dictionary_1_path, mode="r") as d1:
        dictionary_1 = [l.lower().rstrip() for l in d1.readlines()]
    print(f"Reading in {dictionary_2_path}...")
    with open(dictionary_2_path, mode="r") as d2:
        dictionary_2 = [l.lower().rstrip() for l in d2.readlines()]

    # Print the length of each dictionary:
    print(f"\nDictionary 1 has {len(dictionary_1)} entries.")
    print(f"Dictionary 2 has {len(dictionary_2)} entries.")

    # De-dup and merge the two dictionaries
    print("\nDe-duplicating the two dictionaries and merging them.")
    merged_dictionary = [word for word in set(dictionary_1).union(set(dictionary_2))]
    print(f"There are { len(merged_dictionary) } unique words between the two dictionaries.")

    # Print 5 random words:
    print("\nPrinting 5 random words from the merged dictionary:")
    for i in range(0, 5):
        print(f"\tRandom word number { i }: { merged_dictionary[random.randint(0,len(merged_dictionary))]}")

    # Print 5 more random words:
    print("\nPrinting 5 MORE random words from the merged dictionary:")
    for (i, word) in enumerate(random.sample(merged_dictionary, 5)):
        print(f"\tRandom word number { i }: { word }")

    # Find all words that start with `a`:
    a_words = [word for word in merged_dictionary if word[0] == "a"]
    # Optional alternate: a_words = [word for word in merged_dictionary if word.startswith("a")]
    print(f"\nThere are { len(a_words) } words in the merged dictionary that start with `a`.")

    # How many words start with each letter of the alphabet:
    print("\nPrinting how many words start with each letter:")
    for letter in word_count(dictionary=merged_dictionary):
        print(f"\t{ letter[0] }: { letter[1] }")


def word_count(dictionary: list) -> tuple:
    """
    Given the list of words, yield a tuple of (letter, number_of_words_starting_with_that_letter) with each iteration
    :param dictionary:
    :yield: (letter, number_of_words_starting_with_that_letter)
    """

    for letter in ascii_lowercase:
        yield (letter, len([word for word in dictionary if word[0] == letter]))


if __name__ == "__main__":
    main()
