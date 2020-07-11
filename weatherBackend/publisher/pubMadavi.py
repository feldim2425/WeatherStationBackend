from .pubSenseComREST import PubSensComREST, PinType

class PubMadavi(PubSensComREST):
	
	def __init__(self, id):
		super().__init__(id, "http://api-rrd.madavi.de/data.php", "Madavi", PinType.PREFIX)