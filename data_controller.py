#!/bin/python
# -*- coding: utf-8 -*-

from data import Data
from data_node import DataNode
from typing import List


class DataNodeController(object):
    """
    Controlling class for DataNodes
    """
    def create_node_hierarchy(self, data_list: List[Data]) -> DataNode:
        """
        Creates node based on list of Data.
        First
        :param data_list: list of Data
        :return: list of DataNode
        """
        nodes = []
        for data in data_list:
            nodes.append(DataNode(instance=data))

        self.update_node_hierarchy(nodes)
        return nodes

    def update_node_hierarchy(self,
                              nodes_list: List[DataNode],
                              remove_from_list=False) -> None:
        """
        Updates nodes in list with references parent-child type
        :param nodes_list: nodes for update
        :param remove_from_list: flag for removing from list ex-orphans
        :return: None
        """
        for node in nodes_list:
            if not node.is_orphan_node():
                continue

            for checked_node in nodes_list:
                if self._search_parent(checked_node, node):
                    if remove_from_list:
                        nodes_list.remove(node)
                    break

    def _search_parent(self, checked_node: DataNode, orphan_node: DataNode) -> bool:
        """
        Searches parent for orphan node in node and it children
        :param checked_node: node for searching parent
        :param orphan_node: parentless node
        :return: True if parent found
        """
        if orphan_node.get_parent_node() is not None:
            return True

        if checked_node.get_id() == orphan_node.get_parent_id():
            checked_node.append_child(orphan_node)
            return True

        for child in checked_node.get_children():
            if self._search_parent(child, orphan_node):
                return True
        return False

    def to_data_list(self, node: DataNode) -> List[Data]:
        """
        Extracts data from DataNodes into list
        :param node: DataNode for extracting
        :return: list of Data
        """
        return self._to_data_list(node, [])

    def _to_data_list(self, node: DataNode, list_: List[Data]) -> List[Data]:
        """
        Recursive method for extracting Data from DataNode
        :param node: node for extracting
        :param list_: container for extracted Data
        :return: updated list with extracted Data
        """
        list_.append(node.get_instance())
        child_items = []
        for child in node.get_children():
            self._to_data_list(child, list_)
        list_.extend(child_items)
        return list_
