#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_multi` -- Investigate multiprocessing / multithreading
=========================================

LAB_multi Learning Objective: Learn to use the multiprocessing and multithreading modules
                              to perform parallel tasks.
::

 a. Create set of three functions that perform the following tasks:
    1. Capitalize all strings that come through and pass them along
    2. Count the number of characters in the string and pass along the string and the count as a
       a tuple (string, count).
    3. Check to see if the count is the largest seen so far.  If so, send along a tuple with
       (string, count, True), else send (string, count, False)

 b. Spawn each of those functions into processes (multiprocessing) and wire them together
    with interprocess communications (queues).

 c. Run the entire data/dictionary2.txt file through your processing engine, one word at a time.

 d. In the main process, monitor the results coming from the last stage in the processing engine.
    After all the words have been processed, print the longest word that went through the engine.

 e. If you complete the above tasks, go back and do the same tasks using threads (threading).  Don't
    delete your multiprocessing code, just add the threading code.

"""

import asyncio
import multiprocessing
import threading
import time


def main():
    """
    doin stuff and thangs
    :return:
    """

    print("\n======== [ STARTING TESTING ] ========\n")
    print("Gathering the dictionary")
    dictionary_1_path = "/Users/bret7530/Documents/scripts/Envs/RU_Python_IV/data/dictionary1.txt"
    dictionary_2_path = "/Users/bret7530/Documents/scripts/Envs/RU_Python_IV/data/dictionary2.txt"

    # Grab the dictionaries
    print(f"Reading in { dictionary_1_path }...")
    with open(dictionary_1_path, mode="r") as d1:
        dictionary_1 = [str(l).lower().rstrip() for l in d1.readlines()]
    print(f"Reading in {dictionary_2_path}...")
    with open(dictionary_2_path, mode="r") as d2:
        dictionary_2 = [str(l).lower().rstrip() for l in d2.readlines()]

    # Print the length of each dictionary:
    print(f"\nDictionary 1 has {len(dictionary_1)} entries.")
    print(f"Dictionary 2 has {len(dictionary_2)} entries.")

    # De-dup and merge the two dictionaries
    print("\nDe-duplicating the two dictionaries and merging them.")
    dictionary = [word for word in set(dictionary_1).union(set(dictionary_2))]
    print(f"Dictionary of {len(dictionary)} words ingested...")

    print("Plumbing up queues")
    capital_queue = multiprocessing.JoinableQueue(maxsize=10000)
    counter_queue = multiprocessing.JoinableQueue(maxsize=10000)
    longest_queue = multiprocessing.JoinableQueue(maxsize=10000)
    final_queue = multiprocessing.JoinableQueue(maxsize=10000)

    async_capital_queue = asyncio.Queue()
    async_counter_queue = asyncio.Queue()
    async_longest_queue = asyncio.Queue()
    async_final_queue = asyncio.Queue()

    print("Setup our processes")
    capital_process = multiprocessing.Process(target=capitalizer, args=[capital_queue, counter_queue])
    capital_process.daemon = True
    capital_process.start()

    counter_process = multiprocessing.Process(target=counter, args=[counter_queue, longest_queue])
    counter_process.daemon = True
    counter_process.start()

    longest_process = multiprocessing.Process(target=longest, args=[longest_queue, final_queue])
    longest_process.daemon = True
    longest_process.start()

    feeder_process = multiprocessing.Process(target=feeder, args=[dictionary, capital_queue])
    feeder_process.daemon = True
    # Not starting it until we're testing in a second.

    print("Start our threads")
    capital_thread = threading.Thread(target=capitalizer, args=[capital_queue, counter_queue])
    capital_thread.daemon = True
    capital_thread.start()

    counter_thread = threading.Thread(target=counter, args=[counter_queue, longest_queue])
    counter_thread.daemon = True
    counter_thread.start()

    longest_thread = threading.Thread(target=longest, args=[longest_queue, final_queue])
    longest_thread.daemon = True
    longest_thread.start()

    feeder_thread = threading.Thread(target=feeder, args=[dictionary, capital_queue])
    feeder_thread.daemon = True
    # Not starting it until we're testing in a second.

    print("Start our Asyncio Event Loop")
    loop = asyncio.get_event_loop()

    print("Start our coroutines/Tasks")
    tasks = [
        loop.create_task(async_capitalizer(async_capital_queue, async_counter_queue)),
        loop.create_task(async_counter(async_counter_queue, async_longest_queue)),
        loop.create_task(async_longest(async_longest_queue, async_final_queue)),
    ]

    proc_start = time.time()
    print("\n======== [ TESTING PROCESSES ] ========\n")
    feeder_process.start()

    print("Awaiting the longest word...")
    longest_word = waiter(final_queue)

    # Longest word!
    print(f"{ longest_word[0] } is the longest word in our dictionary at { longest_word[1] } characters!")
    print(f"Processes worked this out in {time.time() - proc_start:.2f} seconds.")

    thread_start = time.time()
    print("\n======== [ TESTING THREADS ] ========\n")
    feeder_thread.start()

    print("Awaiting the longest word...")
    longest_word = waiter(final_queue)

    # Longest word!
    print(f"{ longest_word[0] } is the longest word in our dictionary at { longest_word[1] } characters!")
    print(f"Processes worked this out in {time.time() - thread_start:.2f} seconds.")

    async_start = time.time()
    print("\n======== [ TESTING ASYNCIO ] ========\n")
    loop.run_until_complete(asyncio.gather(async_feeder(dictionary, async_capital_queue)))

    print("Awaiting the longest word...")
    longest_word = loop.run_until_complete(asyncio.gather(async_waiter(async_final_queue)))[0]

    # Longest word!
    print(f"{ longest_word[0] } is the longest word in our dictionary at { longest_word[1] } characters!")
    print(f"Asyncio worked this out in {time.time() - async_start:.2f} seconds.")

    print("Destroying our tasks")
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

    serial_start = time.time()
    print("\n======== [ TESTING SERIAL EXECUTION ] ========\n")
    longest_word = ("", 0, False)
    for word in dictionary:
        upper_word = word.upper()
        word_count = (upper_word, len(upper_word))
        if len(word) >= longest_word[1]:
            longest_word = (word_count[0], word_count[1], True)

    # Longest word!
    print(f"{ longest_word[0] } is the longest word in our dictionary at { longest_word[1] } characters!")
    print(f"Serial execution worked this out in {time.time() - serial_start:.2f} seconds.")


def feeder(dictionary: list, queue: multiprocessing.JoinableQueue):
    """
    Feed your words into a queue
    :param dictionary:
    :param queue:
    :return:
    """

    print("Feeding words into the pipeline")
    count = 0
    for word in dictionary:
        count += 1
        while queue.full():
            # print("Sleeping .0005 seconds to allow queue to empty.")
            time.sleep(.0005)

        queue.put(word)
        if count % 100000 == 0:
            print(f"Placed the {count}th word into the queue.")
            # if count >= 130000:
            #     print(f"Placed the {count}th word, {word}, into the queue.")


def capitalizer(queue: multiprocessing.JoinableQueue, nextqueue: multiprocessing.JoinableQueue):
    while True:
        word = queue.get()
        nextqueue.put(word.upper())
        queue.task_done()


def counter(queue: multiprocessing.JoinableQueue, nextqueue: multiprocessing.JoinableQueue):
    while True:
        word = queue.get()
        nextqueue.put((word, len(word)))
        queue.task_done()


def longest(queue: multiprocessing.JoinableQueue, nextqueue: multiprocessing.JoinableQueue):
    longest_word = ("", 0, False)
    while True:
        word_count = queue.get()
        if word_count[1] >= longest_word[1]:
            longest_word = (word_count[0], word_count[1], True)
            nextqueue.put(longest_word)
        else:
            nextqueue.put((word_count[0], word_count[1], False))
        queue.task_done()


def waiter(queue: multiprocessing.JoinableQueue) -> tuple:
    longest_word = None
    while True:
        results = queue.get()

        if results[2] is True:
            longest_word = results
        queue.task_done()

        if queue.empty():
            print("Final queue is empty, waiting 1 second to be sure it's REALLY empty.")
            time.sleep(1)
            if queue.empty():
                break

    return longest_word


async def async_feeder(dictionary: list, queue: asyncio.Queue):
    """
    Feed your words into a queue
    :param dictionary:
    :param queue:
    :return:
    """

    print("Feeding words into the pipeline")
    count = 0
    for word in dictionary:
        count += 1
        while queue.full():
            print("Sleeping 1 seconds to allow queue to empty.")
            time.sleep(1)
        else:
            await queue.put(word)
            if count % 100000 == 0:
                print(f"Placed the {count}th word into the queue.")


async def async_capitalizer(queue: asyncio.Queue, nextqueue: asyncio.Queue):
    while True:
        word = await queue.get()
        await nextqueue.put(word.upper())
        queue.task_done()


async def async_counter(queue: asyncio.Queue, nextqueue: asyncio.Queue):
    while True:
        word = await queue.get()
        await nextqueue.put((word, len(word)))
        queue.task_done()


async def async_longest(queue: asyncio.Queue, nextqueue: asyncio.Queue):
    longest_word = ("", 0, False)
    while True:
        word_count = await queue.get()
        if word_count[1] >= longest_word[1]:
            longest_word = (word_count[0], word_count[1], True)
            await nextqueue.put(longest_word)
        else:
            await nextqueue.put((word_count[0], word_count[1], False))
        queue.task_done()


async def async_waiter(queue: asyncio.Queue) -> tuple:
    longest_word = None
    while True:
        results = await queue.get()

        if results[2] is True:
            longest_word = results
        queue.task_done()

        if queue.empty():
            break

    return longest_word


if __name__ == '__main__':
    main()
