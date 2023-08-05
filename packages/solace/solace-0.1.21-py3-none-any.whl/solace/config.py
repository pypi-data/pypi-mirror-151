import os
import json
import yaml
from box import Box
from .utils.ymlutils import Loader
from cerberus import Validator
from .exceptions import AppConfigurationError

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class SolaceAppConfigFromYml:
    """ 
    This class provides Solace App Config 
    loaded from a YML file.
    """
    def __init__(self, yml_file: str):

        with open(yml_file, 'r') as f:
            self.app_config = yaml.load(f, Loader=Loader)
    
    def __validate(self):
        """ validates the appconfig against the app config schema """
        with open(f"{DIR_PATH}/app_config_schema.yml", 'r') as f:
            app_config_schema = yaml.safe_load(f)
        self.v = Validator(app_config_schema)
        is_valid = self.v.validate(self.app_config)
        if not is_valid:
            errors = yaml.dump(self.v.errors, default_flow_style=False)
            raise AppConfigurationError(f"Invalid App Configuration:\n {errors}")

    def __call__(self):
        self.__validate()
        return Box(self.app_config)