#!/bin/python
# -*- coding: utf-8 -*-

import json
from data import Data


class DataEncoder(json.JSONEncoder):
    """
    Class for encoding Data to JSON format
    """
    def default(self, value):
        if isinstance(value, Data):
            return {
                "__data__": True,
                "id": value.get_id(),
                "value": value.get_value(),
                "enabled": value.is_enabled(),
                "parent_id": value.get_parent_id()
            }
        else:
            super().default(self. value)


class DataDecoder(json.JSONDecoder):
    """
    Class for decoding Data from JSON format
    """
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "__data__" in obj:
            id_ = int(obj["id"])
            value = obj["value"]
            enabled = bool(obj["enabled"])
            parent_id = int(obj["parent_id"]) if obj["parent_id"] is not None else None
            return Data(value=value, parent_id=parent_id, id_=id_, enabled=enabled)

        return obj
