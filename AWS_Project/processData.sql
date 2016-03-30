INSERT INTO `aqiq_processed`(`userid`, `session_id`, `Rtc Date (GMT)`,
`Rtc Time (GMT)`,`BMP Pres(mb)`,`SHT25 Temp(C)`,`SHT25 Humidity`,
`CO2(ppm)`,`Wind Speed(mph)`,`Wind Direction(deg)`,`Quad-Aux1`,
`Quad-Main1`,`Quad-Aux2`,`Quad-Main2`,`Quad-Aux3`,`Quad-Main3`,
`Quad-Aux4`,`Quad-Main4`, `Fig 210 Heat`,`Fig 210 Sens`,`Fig 280 Heat`,
`Fig 280 Sens`,`BL Moccon`,`E2VO3(heat)`, 'E2VO3(sens)', 'GPS Date',
'GPS Time (UTC?)','Latitude','Longitude', 'Fix Quality',
'Altitude(meters above sea level)', 'Satellites')
SELECT `Rtc Date`,
`Rtc Time`,
(`BMP Temp(C)`*9.0)/5.0, #example to convert C to F, doesn't actually need to be converted
`BMP Pres(mb)`, #no conver.
`SHT25 Temp(C)`, #no conver.
`SHT25 Humidity`, #no conver.
`CO2(ADC VAL)`, #conver.
`Wind Speed(mph)`, #no conver.
`Wind Direction(deg)`, #no conver.
`Quad-Aux-1(microVolts)`,#conver.?
`Quad-Main-1(microVolts)`,#conver.?
`Quad-Aux-2(microVolts)`,#conver.?
`Quad-Main-2(microVolts)`,#conver.?
`Quad-Aux-3(microVolts)`,#nconver.?
`Quad-Main-3(microVolts)`,#conver.?
`Quad-Aux-4(microVolts)`,#conver.?
`Quad-Main-4(microVolts)`,#conver.?
`Fig 210 Heat(milliVolts)`,#conver.?
`Fig 210 Sens(milliVolts)`,#conver.
`Fig 280 Heat(milliVolts)`,#conver.?
`Fig 280 Sens(milliVolts)`,#conver.
`BL Moccon sens(milliVolts)`,#conver.
`E2VO3 Heat(milliVolts)`,#conver.?
`E2VO3 Sens(milliVolts)`,#conver.
`GPS Date`,#no conver.
`GPS Time(UTC)`,#no conver.
`Latitude`,#no conver.
`Longitude`,#no conver.
`Fix Quality`,#no conver.
`Altitude(meters above sea level)`,#no conver.
`Statellites`#no conver.
FROM `aqiq_raw` 
