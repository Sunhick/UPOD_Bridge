"""
Parser.py

Parse the GPS data
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.2.0"
__email__ = "suba5417@colorado.edu"

import logging

from GGAParser import GGAParser

# log = logging.getLogger(__name__)

class Parser(object):
    @staticmethod
    def parse(gps):
        """ Parse the GPS NEMA string """
        tokens = gps.split(',')
        id = tokens[0]

        if not id:
            return GGAParser()

        if id == '$GPGGA':
            gga = GGAParser()
            gga.parse(tokens)

            return gga
        if id == '$GPGSA':
            pass
        if id == '$GPGSV':
            pass
        if id == '$GPRMC':
            pass
