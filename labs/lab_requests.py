#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_requests` -- interacting with REST
=========================================

LAB_REQUESTS Learning Objective: Learn to interact with RESTful APIs using requests library
::

 a. Using requests, HTTP GET the initial page from the url given to you by the instructor.

 b. Using the JSON you receive from the server, determine the next url you are to open.
    Use HTTP POST to send the `token` you received from the initial page back to the server
    at the next url to load the second page.

    The returned JSON object will be in the form: {'next': url, 'token': <your_token>}
    where the value for the 'next' key is the url you should post to next, and <your_token> will
    be the same token you sent to the server.

    Your post JSON should be only one element: {'token': <your_token>}

 c. Continue the pattern from step b until you get a JSON response that contains the element
    called `answer`.  Print out the final object you recieved from the server.

 Note: the token has a short timeout, so you will have to pull all the steps in a loop,
       otherwise the token will invalidate due to timeout

 d. (Optional) If you want more of a challenge, head to the advanced URL given by the instructor.
    Note that for this challenging API the JSON objects returned have a random key for the url and
    the token returned for each response.  You will have to determine how to get the url from the
    JSON response object.

"""

import requests  # noqa

# Load the first page using an HTTP GET
# Begin loop:
#     parse the JSON object to find the next url
#     load the url using an HTTP POST
#     stop the loop when the JSON object has the key: "answer"
# Print the final JSON response

# Note: if you need to debug your HTTP connection info, call the following
# function before you do any http calls with requests:


def debug_mode():
    import logging
    from http.client import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def main():
    """
    requesting stuff
    :return:
    """

    print("========[ TRYING THE BASIC URL ] ========\n")
    initial_url = "http://104.239.140.227"
    print(f"Making initial request to {initial_url}")
    response = requests.get(initial_url)
    r_json = response.json()
    token = r_json["token"]
    print(f"Token: {token}")
    url = r_json["next"]
    print(f"Next URL: {url}")

    print("Following the trail...")
    counter = 0
    while True:
        counter = counter + 1
        next_response = requests.post(url, json={"token": token})
        next_json = next_response.json()
        answer = next_json.get("answer")
        if not answer:
            print(f"Looping on to try number {counter}")
            url = next_json["next"]
        else:
            break

    print(f"Final response: {next_json}")

    print("\n========[ TRYING THE ADVANCED URL ] ========\n")

    initial_url = "http://104.239.140.227/advanced"
    print(f"Making initial request to {initial_url}")
    response = requests.get(initial_url)
    r_json = response.json()
    token = r_json["token"]
    print(f"Token: {token}")
    next_url = None
    for key in r_json.keys():
        if key != "token":
            next_url = key
            continue
    url = r_json[next_url]
    print(f"Next URL ({next_url}): {url}")

    print("Following the trail...")
    counter = 0
    while True:
        counter = counter + 1
        next_response = requests.post(url, json={"token": token})
        next_json = next_response.json()
        answer = next_json.get("answer")
        if not answer:
            print(f"Looping on to try number {counter}")
            next_url = None
            for key in next_json.keys():
                if key != "token":
                    next_url = key
                    continue
            url = next_json[next_url]
            print(f"Next URL ({next_url}): {url}")
        else:
            break

    print(f"Final response: {next_json}")


if __name__ == '__main__':
    main()
