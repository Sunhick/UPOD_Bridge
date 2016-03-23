"""
TxtWriter.py

Plain Txt file writer and rotating csv file writer

"""

__author__ = "Sunil"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.2.0"
__email__ = "suba5417@colorado.edu"

import os
import csv
import time        
import devices
# import logging

_MIDNIGHT = 24 * 60 * 60  # number of seconds in a day

class TxtWriter(object):
    write_header = True
    
    def __init__(self, filename):
        # self.log = logging.getLogger(__name__)
        self.header = ('Rtc Date', 'Rtc Time', 'BMP Temp(C)', 'BMP Pres(mb)',
                       'SHT25 Temp(C)', 'SHT25 Humidity', 'CO2(ADC VAL)', 'Wind Speed(mph)',
                       'Wind Direction(deg)', 'Quad-Aux-1(microVolts)', 'Quad-Main-1(microVolts)',
                       'Quad-Aux-2(microVolts)','Quad-Main-2(microVolts)', 'Quad-Aux-3(microVolts)',
                       'Quad-Main-3(microVolts)', 'Quad-Aux-4(microVolts)', 'Quad-Main-4(microVolts)',
                       'Fig 210 Heat(milliVolts)', 'Fig 210 Sens(milliVolts)',
                       'Fig 280 Heat(milliVolts)', 'Fig 280 Sens(milliVolts)', 'BL Moccon sens(milliVolts)',
                       'ADC2 Channel-2(empty)', 'E2VO3 Heat(milliVolts)', 'E2VO3 Sens(milliVolts)',
                       'GPS Date', 'GPS Time(UTC)', 'Latitude','Longitude',
                       'Fix Quality', 'Altitude(meters above sea level)', 'Statellites', 'Digital Pin-3(ADC Value)', 
                       'Digital Pin-4(ADC Value)','Digital Pin-5(ADC Value)')
        self.filename = filename


    def _open(self):
      # Fix this hard coded path for detecting the usb moubt
      # use dmesg maybe
      mp = devices.get_mount_points()
      # last device mounted path
      if mp and len(mp) > 0:
        dev = mp[len(mp)-1][1]
      else: dev = 'sda1'

      mountpath =  os.path.join(dev, 'arduino') #'{device}/arduino/'.format(device=dev)
      mount =  os.path.join(mountpath, 'mount.txt')
      print 'mount:' , mount
      upodfile = os.path.join(mountpath, self.filename)

      if not os.path.exists(mount):
        print 'no file'
        return None

      exists = os.path.exists(upodfile)
      stream = open(upodfile, 'a')

      writer = csv.writer(stream)
      # write header if it's a new file
      if not exists:
        writer.writerow(self.header)

      return stream

    def write(self, sensor):
        # If the sd card is not mounted then don't log
        stream = self._open()

        if not stream:
          return False

        try:
            writer = csv.writer(stream)
            writer.writerow((sensor.RtcDate,
                                  sensor.RtcTime,
                                  sensor.BmpTemperature,
                                  sensor.BmpPressure,
                                  sensor.Sht25Temperature,
                                  sensor.Sht25Humidity,
                                  sensor.CO2,
                                  sensor.WindSpeed,
                                  sensor.WindDirection,
                                  sensor.Quad_Aux1,
                                  sensor.Quad_Main1,
                                  sensor.Quad_Aux2,
                                  sensor.Quad_Main2,
                                  sensor.Quad_Aux3,
                                  sensor.Quad_Main3,
                                  sensor.Quad_Aux4,
                                  sensor.Quad_Main4,
                                  sensor.Fig210_Heat,
                                  sensor.Fig210_Sens,
                                  sensor.Fig280_Heat,
                                  sensor.Fig280_Sens,
                                  sensor.BL_Mocon_Sens,
                                  sensor.Adc2_Channel_2,
                                  sensor.E2VO3_Heat,
                                  sensor.E2VO3_Sens,
                                  sensor.GpsData.Utc,
                                  sensor.GpsData.Utc,
                                  sensor.GpsData.Latitude,
                                  sensor.GpsData.Longitude,
                                  sensor.GpsData.FixQuality,
                                  sensor.GpsData.Altitude,
                                  sensor.GpsData.Satellites,
                                  sensor.Dpin3, 
                                  sensor.Dpin4, 
                                  sensor.Dpin5))
            return True
        except Exception, e:
            #self.log.exception(e)
            return False
        finally:
            if stream:
              stream.flush()
              stream.close()


class RotatingTxtWriter(TxtWriter):
    """
    Rotating csv file writer
    """
    def __init__(self, filename):
        TxtWriter.__init__(self, filename)
        self.interval = 60 * 60 * 24 # one day
        self.suffix = "%Y-%m-%d"
        t = int(time.time())
        self.roll_over_at = self._compute_roll_over_at(t)

    def _compute_roll_over_at(self, currentTime):
        """
        Work out the rollover time based on the specified time.
        """
        result = currentTime + self.interval
        t = time.localtime(currentTime)
        currentHour = t[3]
        currentMinute = t[4]
        currentSecond = t[5]
        # r is the number of seconds left between now and midnight
        r = _MIDNIGHT - ((currentHour * 60 + currentMinute) * 60 +
                         currentSecond)
        result = currentTime + r
        return result

    def write(self, sensor):
        try:
            if self.should_roll_over(sensor):
                self.do_roll_over()
            return TxtWriter.write(self, sensor)
        except Exception, e:
            pass
            #self.log.exception(e)

    def should_roll_over(self, sensor):
        """
        Determine if rollover should occur.
        """
        t = int(time.time())
        return t >= self.roll_over_at

    def do_roll_over(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()

        t = self.roll_over_at - self.interval
        timeTuple = time.localtime(t)
        #dfn = self.filename + "." + time.strftime(self.suffix, timeTuple)
        #if os.path.exists(dfn):
        #    os.remove(dfn)
        #os.rename(self.filename, dfn)
        self.stream = self._open()

        currentTime = int(time.time())
        newRolloverAt = self._compute_roll_over_at(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        dstNow = time.localtime(currentTime)[-1]
        dstAtRollover = time.localtime(newRolloverAt)[-1]
        if dstNow != dstAtRollover:
            if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                newRolloverAt = newRolloverAt - 3600
            else:           # DST bows out before next rollover, so we need to add an hour
                newRolloverAt = newRolloverAt + 3600
        self.roll_over_at = newRolloverAt
