from .pubSenseComREST import PubSensComREST

class PubLuftdaten(PubSensComREST):
	
	def __init__(self, id):
		super().__init__(id, "http://api.sensor.community/v1/push-sensor-data/", "Luftdaten.info")