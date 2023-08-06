from cerberus import Validator
from typing import Any
# TODO: read up on Cerberus and extend functionality of this validator helper

class SolaceValidator:
    allow_unknown: bool = False
    require_all: bool = False

    def __init__(self, schema: dict):
        self.schema = schema
        self.validator = Validator()
    
    @property
    def errors(self):
        return self.validator.errors
    
    @property
    def data(self):
        return self.validator.validated(self.payload, self.schema)
    
    def get(self, property: str, default: Any = None):
        if property in self.data:
            return self.data.get(property)
        return default

    def __call__(self, payload: dict):
        self.payload = payload
        self.validator.allow_unknown = self.allow_unknown
        self.validator.require_all = self.require_all
        return self.validator.validate(payload, self.schema)
