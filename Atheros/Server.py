 #!/usr/bin/python

"""
server.py

Read the data from the ATMega and post to processing Queue thread
"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.2.0"
__email__ = "suba5417@colorado.edu"

import sys
import os

# import path
sys.path.insert(0, '/usr/lib/python2.7/bridge')  

import devices
import Queue
import time
import signal
import threading
import logging
import logging.config

from datetime import datetime
from Processor import DataProcessor, queue
from bridgeclient import BridgeClient as bridgeclient

# set up the logging
# print('Setting up logging module...')
basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

logging.config.fileConfig('%s/logging.conf' % basepath)

log = logging.getLogger(__name__)


def signal_handler(signal, frame):
    """ clean up data on Signal interrupt """
    # log.info('Exiting Server on signal interrupt')
    sys.exit(0)

def main(*argv):
    # set the current thread id
    threading.current_thread().name = 'Server-Thread'

    # install signal handler
    signal.signal(signal.SIGINT, signal_handler)
    # log.info('Installed signal handler')

    # setup event for thread synchronization
    event = threading.Event()

    # get communication channel to ATMega
    channel = bridgeclient()

    # setup data processing thread
    processor = DataProcessor(name='DataProcessor-Thread', event=event, bridge=channel)
    processor.start()
    # log.info('Launched Data processor thread')

    
    if not channel:
        # log.critical('unable to setup bridgeclient to ATMega!')
        return

    # TODO: Explore BridgeClient code
    # Performance: keep the socket open while subsequent get(...) operations
    # By default BridgeClient open socket at begin of get(...) and closes after get(...)
    channel.should_close_at_function_end = False

    last_seen = ''
    # Get data from the Tx-channel and post it the queue
    while True:
        try:
            data = channel.get('TX-channel')

            mp = devices.get_mount_points()
            status = 'F'
            if len(mp) > 0:
                status = 'T'

            channel.put('status', status)
            # Time stamp is a part of data contract between
            # ATMega and Atheros. This makes sure that data
            # is different from that of previous data

            # Prevent duplicate data read on the bridgeclient before it's refeshed
            if data == last_seen:
                continue

            queue.put(data)
            last_seen = data
            event.set()
        except Exception, e:
            # log.exception(e)
            # log.warning('Continue by ignoring the above exception!')
            # try to re-initialize the ATMega communication channel
            channel = bridgeclient()
            processor.channel = channel

        time.sleep(.7)


if __name__ == '__main__':
    main(sys.argv)
