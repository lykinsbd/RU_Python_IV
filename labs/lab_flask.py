#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_flask` -- serving up REST
=========================================

LAB_FLASK Learning Objective: Learn to serve RESTful APIs using the Flask library
::

 a. Using Flask create a simple server that serves the following string for the root route ('/'):
  "<h1>Welcome to my server</h1>"

 b. Add a route for "/now" that returns the current date and time in string format.

 c. Add a route that converts Fahrenheit to Centigrade and accepts the value to convert
    in the url.  For instance, /fahrenheit/32.0 should return "0.0"

 d. Add a route that converts Centigrade to Fahrenheit and accepts the value to convert
    in the url.  For instance, /centigrade/0.0 should return "32.0"

"""

import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Welcome to my world!</h1>"


@app.route("/now")
def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z")


@app.route("/fahrenheit/<int:f_temp>")
@app.route("/fahrenheit/<float:f_temp>")
def f_to_c(f_temp):
    """
    convert Fahrenheit to Centigrade
    :param f_temp:
    :type f_temp: int
    :return: c_temp
    :rtype: int
    """

    c_temp = 5.0 / 9.0 * (f_temp - 32)
    return str(c_temp)


@app.route("/centigrade/<int:c_temp>")
@app.route("/centigrade/<float:c_temp>")
def c_to_f(c_temp):
    """
    convert Centigrade to Fahrenheit
    :param c_temp:
    :type c_temp: int
    :return: f_temp
    :rtype: int
    """

    f_temp = (c_temp * 9.0 / 5.0) + 32
    return str(f_temp)


if __name__ == '__main__':
    app.run()
