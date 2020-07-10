from .publisher import Publisher
import json
import asyncio
import aiohttp
import logging

logger = logging.getLogger("SensorCommunityREST Publisher")

# More info: https://github.com/opendata-stuttgart/meta/wiki/APIs
_LUFTDATEN_XPINS = {
	"bme280": "11",
	"sds011": "1"
}

class PubSensComREST(Publisher):
	
	def __init__(self, id, url, name):
		self.__id = id
		self.__url = url
		self.__valid = id != None
		if not self.__valid:
			logger.warning("Sensor ID for %s is not set correctly", name)

	def handleData(self, data):
		logger.log(logging.DEBUG, "Recieved valid data")
		
		if self.__valid:
			asyncio.ensure_future(self._sendData(data))

	async def _sendData(self, data):
		async with aiohttp.ClientSession() as session:
			if ("temp" in data) and ("humid" in data) and ("pressure" in data):
				await session.request(method = "POST", url = self.__url, headers = {
					"content-type": "application/json",
					"X-Pin": _LUFTDATEN_XPINS['bme280'],
					"X-Sensor": self.__id
				}, json = {
				"sensordatavalues":[
					{"value_type":"temperature","value":"{val:.2f}".format(val=data["temp"])},
					{"value_type":"humidity","value":"{val:.2f}".format(val=data["humid"])},
					{"value_type":"pressure","value":"{val:.2f}".format(val=data["pressure"] * 100)}
				]})
			
			if ("pm25" in data) and ("pm10" in data):
				await session.request(method = "POST", url = self.__url, headers = {
					"content-type": "application/json",
					"X-Pin": _LUFTDATEN_XPINS['sds011'],
					"X-Sensor": self.__id
				}, json = {
				"sensordatavalues":[
					{"value_type":"P1","value":"{val:.2f}".format(val=data["pm10"])},
					{"value_type":"P2","value":"{val:.2f}".format(val=data["pm25"])}
				]})