from .publisher import Publisher
import json
import asyncio
import aiohttp
import logging
from enum import Enum

logger = logging.getLogger("SensorCommunityREST Publisher")

# More info: https://github.com/opendata-stuttgart/meta/wiki/APIs
_LUFTDATEN_XPINS = {
	"bme280": "11",
	"sds011": "1"
}

class PinType(Enum):
	NONE = 0
	HEADER = 1
	PREFIX = 2

class PubSensComREST(Publisher):
	
	def __init__(self, id, url, name, pintype = PinType.HEADER):
		self.__id = id
		self.__url = url
		self.__valid = id != None
		self.__pintype = pintype if isinstance(pintype, PinType) else PinType.HEADER
		if not self.__valid:
			logger.warning("Sensor ID for %s is not set correctly", name)

	def handleData(self, data):
		logger.log(logging.DEBUG, "Recieved valid data")
		
		if self.__valid:
			asyncio.ensure_future(self._sendData(data))

	async def _sendData(self, data):
		async with aiohttp.ClientSession() as session:
			header = {
				"content-type": "application/json",
				"X-Sensor": self.__id
			}

			if ("temp" in data) and ("humid" in data) and ("pressure" in data):
				header_thp = header.copy()
				sens_prefix = ''
				if self.__pintype == PinType.HEADER:
					header_thp['X-Pin'] = _LUFTDATEN_XPINS['bme280']
				elif self.__pintype == PinType.PREFIX:
					sens_prefix = 'BME280_'

				await session.request(method = "POST", url = self.__url, headers = header_thp, json = {
				"sensordatavalues":[
					{"value_type":"{}temperature".format(sens_prefix) ,"value":"{val:.2f}".format(val=data["temp"])},
					{"value_type":"{}humidity".format(sens_prefix) ,"value":"{val:.2f}".format(val=data["humid"])},
					{"value_type":"{}pressure".format(sens_prefix) ,"value":"{val:.2f}".format(val=data["pressure"] * 100)}
				]})
			
			if ("pm25" in data) and ("pm10" in data):
				header_pm = header.copy()
				sens_prefix = ''
				if self.__pintype == PinType.HEADER:
					header_pm['X-Pin'] = _LUFTDATEN_XPINS['sds011']
				elif self.__pintype == PinType.PREFIX:
					sens_prefix = 'SDS011_'
				
				await session.request(method = "POST", url = self.__url, headers = header_pm, json = {
				"sensordatavalues":[
					{"value_type":"{}P1".format(sens_prefix), "value":"{val:.2f}".format(val=data["pm10"])},
					{"value_type":"{}P2".format(sens_prefix),"value":"{val:.2f}".format(val=data["pm25"])}
				]})