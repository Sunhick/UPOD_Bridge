"""
DataProcessor.py

Get data from the queue and process it.
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.2.0"
__email__ = "suba5417@colorado.edu"


import Queue
import threading
# import logging
import time

from datetime import datetime
from SensorData import SensorData
from TxtWriter import RotatingTxtWriter
from TxtWriter import TxtWriter
# from pprint import pprint

global queue


BUFFSIZE = 1000
queue = Queue.Queue(BUFFSIZE)
DELIMITER = '#'
DATE_TIME = 0

class DataProcessor(threading.Thread):
    """
    Data processor
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, event=None, bridge=None):
        super(DataProcessor,self).__init__()
        self.target = target
        self.name = name
        self.setDaemon(True)
        self.event = event
        # self.log = logging.getLogger(__name__)
        self.TxtFileCreated = False
        self._file = None
        self.channel = bridge

    def run(self):        
        # get data and process it
        while True:
            # wait for the data to be put in queue
            # if queue is empty. Otherwise process queue
            if queue.empty():
                # self.log.info('Waiting for data to be populated into the queue')
                self.event.wait()

            data = queue.get()
            self.process(data)

    def process(self, data):
        # avoid processing empty data
        if not data:
            # self.log.error('Ignoring empty data processing')
            return

        # self.log.debug('Processing {data}'.format(data=data))

        tokens = data.split(DELIMITER)
        sensor_data = SensorData(tokens)

        # if file not created then create it.
        # Stop gap fix for date & time not set in Atheros
        # Sync the time between Atheros and ATMega
        # UPODXX... xx has to be replaced with POD serial number
        if not self._file:
            dt = float(tokens[DATE_TIME])
            # sychronize Atheros system clock with ATMega
            self.sync_datetime(dt)
            #filename = datetime.fromtimestamp(dt).strftime('UPODXX%d%m%y.txt')
            filename = 'UPODXX.txt'
            # self.log.info('Created file: {name}'.format(name=filename))
            self._file = TxtWriter(filename) # RotatingTxtWriter(filename)

        # pprint(vars(sensor_data))
        # pprint(vars(sensor_data.GpsData))
        # print data
        #status = False
        #while not status:
        status = self._file.write(sensor_data)
            #print status
            # self.channel.put('status', 'T' if status else 'F')
        
    def sync_datetime(self, dt):
        import os
        # see if i need to set hardware clock or system clock
        fdt = datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
        # self.log.info('Setting Atheros date time: {stamp}'.format(stamp=fdt))
        os.system('date -s "{stamp}" > /dev/null 2>&1'.format(stamp=fdt))