#!/bin/python
# -*- coding: utf-8 -*-

import json
from data import DataNode


class DataNodeEncoder(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, DataNode):
            return {
                "__data_node__": True,
                "id": value.get_id(),
                "value": value.get_value(),
                "parent": value.get_parent().get_id() if value.get_parent() is not None else None,
                "children": [self.default(i) for i in value.get_children()],
            }
        else:
            super().default(self. value)


class DataNodeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "__data_node__" in obj:
            node = DataNode(obj["value"])
            node._id = int(obj["id"])
            node._children = self.object_hook(obj["children"])
            children = node.get_children()
            if children:
                [i.set_parent(node) for i in children]

            return node
        return obj
