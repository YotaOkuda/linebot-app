# coding: utf-8

"""
    LINE Messaging API

    This document describes LINE Messaging API.  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic.v1 import BaseModel, Field, StrictStr

class ErrorDetail(BaseModel):
    """
    ErrorDetail
    """
    message: Optional[StrictStr] = Field(None, description="Details of the error. Not included in the response under certain situations.")
    var_property: Optional[StrictStr] = Field(None, alias="property", description="Location of where the error occurred. Returns the JSON field name or query parameter name of the request. Not included in the response under certain situations.")

    __properties = ["message", "property"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ErrorDetail:
        """Create an instance of ErrorDetail from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ErrorDetail:
        """Create an instance of ErrorDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ErrorDetail.parse_obj(obj)

        _obj = ErrorDetail.parse_obj({
            "message": obj.get("message"),
            "var_property": obj.get("property")
        })
        return _obj

