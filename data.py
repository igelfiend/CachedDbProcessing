#!/bin/python
# -*- coding: utf-8 -*-

import uuid


class Data(object):
    """
    Class for store data.
    """
    def __init__(self, value, parent_id=None, id_=None, enabled=True):
        """
        Data constructor.
        In minimum case can be set only with value.
        In additional user can set:
            * parent_id. None if root, otherwise id of the parent Data;
        :param value: stored value;
        :param parent_id: parent id as int.
        """
        self._parent_id = parent_id
        self._enabled = enabled
        self._value = value
        if id_ is None:
            self._id = uuid.uuid4().int
        else:
            self._id = id_

    def __eq__(self, other) -> bool:
        if isinstance(other, Data):
            return self._id == other.get_id()
        return NotImplemented

    def __ne__(self, other) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __repr__(self) -> str:
        """
        Debug-format data representation
        :return: String debug data representation
        """
        return "{{\n"\
               "\tid:        {0},\n"\
               "\tparent_id: {1},\n"\
               "\tvalue:     {2},\n"\
               "}}".format(self._id,
                           self._parent_id,
                           self._value)

    def set_value(self, value) -> None:
        """
        Setting new value of data
        :param value: new value
        :return: None
        """
        self._value = value

    def get_value(self) -> str:
        """
        Getter for receiving value.
        :return: value
        """
        return self._value

    def get_parent_id(self) -> int:
        """
        Getter for receiving parent id.
        :return: Parent id, if no parent None
        """
        return self._parent_id

    def get_id(self) -> int:
        """
        Getter for Data uuid as int
        :return: int uuid of the node
        """
        return self._id

    def set_enabled(self, value) -> None:
        """
        Enables/Disables data
        :param value: flag value
        :return: None
        """
        self._enabled = value

    def is_enabled(self) -> bool:
        """
        Checks if Data is available. Data can be disabled in case of delete.
        :return: False if Data deleted
        """
        return self._enabled

    def set_parent_id(self, parent_id) -> None:
        """
        Setter for parent_id.
        :param parent_id: parent id
        :return: None
        """
        self._parent_id = parent_id
