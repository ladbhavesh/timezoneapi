import configparser
import os

_config = {}

def getConfig(key):

    if _config.get(key) == None:
        basepath = os.path.abspath(os.path.dirname(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(basepath, "settings.ini"))
        val = config['default'][key]

        if val:
            _config[key] = val

        return val
    else:
        val = _config[key]
        if val:
            return val

 

    

