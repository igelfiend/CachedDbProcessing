#!/bin/python
# -*- coding: utf-8 -*-

from data import Data


class DataNodeException(Exception):
    """
    Common exception for DataNode
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class DataNodeInstanceException(DataNodeException):
    """
    That exception raises when incorrect instance passed as argument
    """
    def __init__(self, *args, **kwargs):
        DataNodeException.__init__(self, *args, **kwargs)


class DataNode(object):
    """
    Class for store Tree-type hierarchy of Data.
        * Each DataNode can have any count of DataNode child elements.
        * Each child element will have appropriate parent field value.
        * Root-level Node will have None in parent field
    Class provides proxy interface for access Data
    """
    def __init__(self, value=None, parent=None, instance=None):
        """
        DataNode constructor.
        In minimum case can be set only with value.
        In additional user can set:
            * parent element. In case of setting parent element,
              current element will be appended to that parent element
              children list;
            * instance. When instance set then that instance will be assign to that DataNode.
              Otherwise Data element will be created
        :param value: stored value of the node;
        :param parent: parent element of this node.
        :param instance: Data for that DataNode.
        """
        self._parent = parent

        if instance is not None:
            self._data = instance
        else:
            self._data = Data(value, parent.get_id() if parent is not None else None)

        if parent is not None:
            parent.append_child(self)

        self._children = []

    def __eq__(self, other):
        if isinstance(other, DataNode):
            return self._data == other.get_instance()
        if isinstance(other, Data):
            return self._data == other
        return NotImplemented

    def __ne__(self, other):
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
               "\tchildren: [\n"\
               "{3}\n"\
               "]\n" \
               "}}".format(self.get_id(),
                           self.get_parent_id(),
                           self.get_value(),
                           ",\n".join([repr(i) for i in self._children]))

    def has(self, data) -> bool:
        """
        Checks if node contains entered data
        :param data: Data or DataNode element
        :return: True if node or it children has that data
        """
        if self == data:
            return True

        for child in self._children:
            has_in_child = child.has(data)
            if has_in_child:
                return True

        return False

    def get_children(self):
        """
        Getter for element's children list
        :return: List of the children elements
        """
        return self._children

    def get_instance(self) -> Data:
        """
        Getter for receiving Data reference
        :return: Data reference
        """
        return self._data

    def set_value(self, value) -> None:
        """
        Setting new value for data instance
        :param value: new value
        :return: None
        """
        self._data.set_value(value)

    def get_value(self) -> str:
        """
        Getter for receiving value of the Data.
        :return: value of the node
        """
        return self._data.get_value()

    def get_parent_node(self):
        """
        Getter for receiving parent node reference
        :return: parent DataNode reference
        """
        return self._parent

    def is_orphan_node(self) -> bool:
        """
        Checks if that node hasn't parent
        :return: True when there are no parent for that node
        """
        return self._parent is None

    def get_parent_id(self) -> int:
        """
        Getter for receiving parent if of the Data
        :return: Parent id of the Data as int
        """
        return self._data.get_parent_id()

    def get_id(self) -> int:
        """
        Getter for Data uuid as int
        :return: int uuid of the node
        """
        return self._data.get_id()

    def set_enabled(self, value) -> None:
        """
        Enables/Disables DataNode. Also applies to children
        :param value: enable flag
        :return: None
        """
        self._data.set_enabled(value)
        for child in self.get_children():
            child.set_enabled(value)

    def is_enabled(self) -> bool:
        return self._data.is_enabled()

    def append_child(self, child) -> None:
        """
        Function for appending child element to the node.
        If received not DataNode instance, exception DataNodeInstanceException will be raised.
        :exception DataNodeInstanceException: raised when child type is incorrect.
        :param child: appended child element of the DataNode type
        :return: None
        """
        if isinstance(child, DataNode):
            self._children.append(child)
            child.set_parent(self)
        else:
            raise DataNodeInstanceException

    def set_parent(self, parent) -> None:
        """
        Setter for parent element field.
        :param parent: parent element reference
        :return: None
        """
        self._parent = parent
