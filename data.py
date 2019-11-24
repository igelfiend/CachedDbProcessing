#!/bin/python
# -*- coding: utf-8 -*-

import uuid


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


class DataNodeParentException(DataNodeException):
    """
    That exception raises when child-parent relation was corrupted
    """
    def __init__(self, *args, **kwargs):
        DataNodeException.__init__(self, *args, **kwargs)


class DataNode(object):
    """
    Class for store Tree-type hierarchy data.
        * Each DataNode can have any count of same child elements.
        * Each child element will have appropriate parent field value.
        * Root-level Node will have None in parent field
    """
    def __init__(self, value, parent=None):
        """
        DataNode constructor.
        In minimum case can be set only with value.
        In additional user can set:
            * parent element. In case of setting parent element,
              current element will be appended to that parent element
              children list;
        :param value: stored value of the node;
        :param parent: parent element of this node.
        """
        self._parent = parent

        if isinstance(parent, DataNode) or parent is None:
            if parent is not None:
                parent.append_child(self)
        else:
            raise DataNodeInstanceException

        self._value = value
        self._children = []

        self._id = uuid.uuid4().int

    def __eq__(self, other) -> bool:
        """
        Equal operator. Element only equal if their id is equal
        :param other: another element for equal
        :return: True if elements are equal
        """
        if isinstance(other, DataNode):
            return self._id == other._id
        else:
            return NotImplemented

    def __ne__(self, other) -> bool:
        """
        Not Equal operator. Reverses equal operator.
        :param other: another element for equal
        :return: True if elements not equal
        """
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
               "}}".format(self._id,
                           self._parent.get_id() if self._parent is not None else None,
                           self._value,
                           ",\n".join([repr(i) for i in self._children]))

    def get_children(self) -> list:
        """
        Getter for element's children list
        :return: List of the children elements
        """
        return self._children

    def get_value(self):
        """
        Getter for receiving value of the node.
        :return: value of the node
        """
        return self._value

    def get_parent(self):
        """
        Getter for the parent reference
        If node has no parent element, it will return None
        :return: Parent reference, if no parent None
        """
        return self._parent

    def get_id(self) -> int:
        """
        Getter for node uuid as int
        :return: int uuid of the node
        """
        return self._id

    def append_child(self, child):
        """
        Function for appending child element to the node.
        If received not DataNode instance, exception DataNodeInstanceException will be raised.
        :exception DataNodeInstanceException: raised when child type is incorrect.
        :param child: appended chlid element of the DataNode type
        :return: None
        """
        if isinstance(child, DataNode):
            self._children.append(child)
        else:
            raise DataNodeInstanceException

    def remove_child(self, child):
        """
        Function for removing child element from the node.
        If child element is not type of DataNode, exception DataNodeInstanceException will be raised.
        If child element is not child of processed node, exception DataNodeParentException will be raised.
        :exception DataNodeInstanceException: raised when type of child is incorrect.
        :exception DataNodeParentException: raised when child is not real child of processed node.
        :param child: reference of child for remove.
        :return: None
        """
        if not isinstance(child, DataNode):
            print("Incorrect child for remove received")
            raise DataNodeInstanceException("Object to remove is not required instance")
        if child in self._children:
            self._children.remove(child)
        else:
            print("Trying to remove child from not from it parent")
            raise DataNodeParentException("Child to remove is not child of that element")

    def set_parent(self, parent):
        """
        Setter for parent element field.
        :param parent: parent element pointer
        :return: None
        """
        self._parent = parent

    def delete(self):
        """
        Function for removing processed element from parent element.
        If element has not parent, nothing will be done.
        :return: None
        """
        if self._parent is not None:
            self._parent.remove_child(self)
