#!/usr/bin/env python3
# *-* coding:utf-8 *-*

"""

:mod:`lab_yaml` -- YAML Parsing
=========================================

LAB_YAML Learning Objective: Learn to parse a YAML file using the PyYAML library
                             and use the information.
::

 a. Load the data/widget.yml file using the PyYAML library.

 b. Change the value for the width and height of the window element to be 1/2 their current value.
    Change the size of the text element to be 1/4 it's current value.
    Change the image alignment element to 'justified'.

 c. Save your updated object to widget_updated.yaml using the PyYAML library.

"""

import yaml


def main():
    """
    gettin things done
    :return:
    """

    print("Reading in our YAML")
    with open("/Users/bret7530/Documents/scripts/Envs/RU_Python_IV/data/widget.yml", mode="r") as y:
        widget_yaml = yaml.safe_load(y)

    print("\nChanging the value of width/height in the Window Element.")
    print(f"Current w/h: {widget_yaml['widget']['window']['height']}/{widget_yaml['widget']['window']['width']}")
    widget_yaml["widget"]["window"]["height"] = int(widget_yaml["widget"]["window"]["height"] / 2)
    widget_yaml["widget"]["window"]["width"] = int(widget_yaml["widget"]["window"]["width"] / 2)
    print(f"New w/h: {widget_yaml['widget']['window']['height']}/{widget_yaml['widget']['window']['width']}")

    print("\nChanging the size of the text element to be 1/4 it's current value.")
    print(f"Current text size value: {widget_yaml['widget']['text']['size']}")
    widget_yaml["widget"]["text"]["size"] = int(widget_yaml["widget"]["text"]["size"] / 4)
    print(f"New text size value: {widget_yaml['widget']['text']['size']}")

    print("\nChanging the image alignment element to be 'justified'.")
    print(f"Current image alignment: {widget_yaml['widget']['image']['alignment']}")
    widget_yaml["widget"]["image"]["alignment"] = "justified"
    print(f"New image alignment: {widget_yaml['widget']['image']['alignment']}")

    print("Writing out our new YAML")
    with open("/Users/bret7530/Documents/scripts/Envs/RU_Python_IV/data/widget_updated.yml", mode="w") as y:
        y.write(yaml.safe_dump(widget_yaml))

if __name__ == "__main__":
    main()
