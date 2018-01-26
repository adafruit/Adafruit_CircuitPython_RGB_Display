Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-rgb_display/badge/?version=latest

    :target: https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/

    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

Port of display drivers from https://github.com/adafruit/micropython-adafruit-rgb-display
to Adafruit CircuitPython for use on Adafruit's SAMD21-based and other CircuitPython
boards.

This driver depends on the Adafruit CircuitPython BusDevice module being installed on the
board too: https://github.com/adafruit/Adafruit_MicroPython_BusDevice

Note that this driver currently won't work on micropython.org firmware, instead
you want the micropython-adafruit-rgb-display driver linked above!

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

TODO

API Reference
=============

.. toctree::
   :maxdepth: 2

   api

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-rgb_display --library_location .
