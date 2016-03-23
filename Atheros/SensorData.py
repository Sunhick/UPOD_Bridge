"""
SensorData.py

Parse the ATMega data string into converted Sensor data object
"""

__author__ = "Sunil, Drew Meyers"
__copyright__ = "Copyright 2015, Arduino UPOD Project"
__license__ = "MIT License"
__version__ = "0.2.0"
__email__ = "suba5417@colorado.edu, Drew.Meyers@colorado.edu"

# import logging
import datetime

from GPS import Parser

# log = logging.getLogger(__name__)

MILLIVOLTS_PER_BIT = .1875

class SensorData(object):
    def __init__(self, tokens):
        RTC_token = self._getfloat(tokens[0])
        self.RtcDate = self._get_Unix2UTC_date(RTC_token)
        self.RtcTime = self._get_Unix2UTC_time(RTC_token)

        self.BmpTemperature = self._getfloat(tokens[1])
        self.BmpPressure = self._getfloat(tokens[2])

        self.Sht25Temperature = self._getfloat(tokens[3])
        self.Sht25Humidity = self._getfloat(tokens[4])

        self.CO2 = self._getfloat(tokens[5])

        self.WindSpeed = self._getfloat(tokens[6])
        self.WindDirection = self.ConvertWindDirection(tokens[7])

        self.Quad_Aux1 = self._get_QuatStat_value(tokens[8])
        self.Quad_Aux2 = self._get_QuatStat_value(tokens[10])
        self.Quad_Aux3 = self._get_QuatStat_value(tokens[12])
        self.Quad_Aux4 = self._get_QuatStat_value(tokens[14])
        
        self.Quad_Main1 = self._get_QuatStat_value(tokens[9])
        self.Quad_Main2 = self._get_QuatStat_value(tokens[11])
        self.Quad_Main3 = self._get_QuatStat_value(tokens[13])
        self.Quad_Main4 = self._get_QuatStat_value(tokens[15])

        self.Fig210_Heat = self._get_ADC_value(tokens[16])
        self.Fig210_Sens = self._get_ADC_value(tokens[17])
        self.Fig280_Heat =  self._get_ADC_value(tokens[18])
        self.Fig280_Sens = self._get_ADC_value(tokens[19])
        self.BL_Mocon_Sens = self._get_ADC_value(tokens[20])
        self.Adc2_Channel_2 = self._get_ADC_value(tokens[21])
        self.E2VO3_Heat = self._get_ADC_value(tokens[22])
        self.E2VO3_Sens = self._get_ADC_value(tokens[23])
        self.GpsData = self._get_gps_data(tokens[24])

        self.Dpin3 = self._getInt(tokens[25])
        self.Dpin4 = self._getInt(tokens[26])
        self.Dpin5 = self._getInt(tokens[27])

    def _getInt(self, data):
        if not data:
            return None
        return int(data)

    def _getfloat(self, data):
        if not data:
            return None
        return float(data)

    def _get_gps_data(self, gps_data):
        if not gps_data:
            pass
            # log.error('Gps data is empty. GPS signal is weak maybe!')
        gps = Parser.parse(str(gps_data))
        return gps

    def _get_QuatStat_value(self, data):
        if not data:
            # log.error('QuatStat value is empty')
            return None

        return float(data)

    def _get_ADC_value(self, data):
        if not data:
            # log.error('ADC value is empty!')
            return None

        return float(data) * MILLIVOLTS_PER_BIT

    def _get_Unix2UTC_date(self, RTC_token):
        return datetime.datetime.fromtimestamp(RTC_token).strftime('%Y-%m-%d')

    def _get_Unix2UTC_time(self, RTC_token):
        return datetime.datetime.fromtimestamp(RTC_token).strftime('%H:%M:%S')

    def ConvertWindDirection(self, WindDirectionToken):
        # The following table is ADC readings for the wind direction sensor output, sorted from low to high.
	# Each threshold is the midpoint between adjacent headings. The output is degrees for that ADC reading.
	# Note that these are not in compass degree order! See Weather Meters datasheet for more information.
        if not WindDirectionToken:
            return None
        adc = int(WindDirectionToken)
        if adc < 380:
            return 113
        if adc < 393:
            return 68
        if adc < 414:
            return 90
	if adc < 456:
            return 158
	if adc < 508:
            return 135
    	if adc < 551:
            return 203
	if adc < 615:
            return 180
	if adc < 680:
            return 23
	if adc < 746:
            return 45
	if adc < 801:
            return 248
	if adc < 833:
            return 225
	if adc < 878:
            return 338
	if adc < 913:
            return 0
	if adc < 940:
            return 293
	if adc < 967:
            return 315
        if adc < 990:
            return 270
        else:
            return -1; #error, disconnected?
