import configparser
import pathlib
import logging

logger = logging.getLogger('Configuration')

_DEFAULT_CONFIG ="""[Mqtt]
## Server host (hostname or ip)
host = localhost

## Server port
port = 1883

## Username for Authentication
## Uncomment to enable authentication (also requires the password field)
## To use this value you also have to set "authenticate" to "user"
;username = someuser

## Password for Authentication
## Uncomment to enable authentication (also requires the user field)
## To use this value you also have to set "authenticate" to "user"
;password = somepassword

[Topics]
## Mqtt topic for weather data
weather = weather

[Services]
## Luftdaten.info enable
luftdateninfo = off

## Luftdaten.info sensor id
## The API also requires a sensortype like: esp8266, raspi, esp32,...
## The type has to match the type in your registration
;luftdateninfo_id = esp8266-000000

## Opensensemap enable
opensensemap = off

## Opensensemap sensorbox id
;opensensemap_box = 00000000

## Opensensemap sensor ids
## The list should be seperated via ","
## The order should be as follows: Temperature, Humidity, Pressure, PM2.5, PM10, Rain
;opensensemap_ids = 0,1,2,3,4,5

"""

def _readMqttConfig(cfg):
    config = {}
    
    cfgMqtt = cfg['Mqtt']
    config['host'] = cfgMqtt.get('host', fallback='localhost')
    config['port'] = cfgMqtt.getint('port', fallback=1883)
    
    config['username'] = cfgMqtt.get('username', fallback=None)
    config['password'] = cfgMqtt.get('password', fallback=None)
    
    config['topics']=[]
    config['topics'].append( cfg['Topics'].get('weather', fallback='weather') )
    return config

def _readServicesConfig(cfg):
    config = {}
    
    cfgServices = cfg['Services']
    config['enable_luftdaten'] = cfgServices.getboolean('luftdateninfo', fallback=False)
    if config['enable_luftdaten']:
        config['luftdaten_id'] = cfgServices.get('luftdateninfo_id', fallback=None)
    
    config['enable_opensensemap'] = cfgServices.getboolean('opensensemap', fallback=False)
    if config['enable_opensensemap']:
        config['opensensemap_boxid'] = cfgServices.get('opensensemap_box', fallback=None)
        config['opensensemap_sensors'] = cfgServices.get('opensensemap_ids', fallback='').split(',')
        
    return config


def readConfiguration(cfgPath = None):
    if cfgPath == None:
        cfgPath = pathlib.Path(".") / "config.ini"
    elif type(cfgPath) == str:
        cfgPath = pathlib.Path(cfgPath)
    cfgPath = cfgPath.resolve()
    logger.info('Loading config \"%s\"', cfgPath)
    cfg = configparser.ConfigParser()
    if not cfgPath.is_file():
        with cfgPath.open("w") as f:
            f.write(_DEFAULT_CONFIG)
    
    with cfgPath.open("r") as f:
        cfg.read_file(f)
    
    pcfg = {}
    pcfg['mqtt'] = _readMqttConfig(cfg)
    pcfg['services'] = _readServicesConfig(cfg)

    return pcfg