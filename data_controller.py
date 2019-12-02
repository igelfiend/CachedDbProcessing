#!/bin/python
# -*- coding: utf-8 -*-

from data import Data
from data_node import DataNode
from data_serializer import DataEncoder, DataDecoder
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
        try:
            i = 0
            while i < len(nodes_list):
                node = nodes_list[i]
                if node.is_orphan_node():
                    for checked_node in nodes_list:
                        if self._search_parent(checked_node, node):
                            if remove_from_list:
                                nodes_list.remove(node)
                                i -= 1
                            break
                i += 1
        except Exception as e:
            print("exception {} raised".format(e))

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
            if not checked_node.is_enabled():
                orphan_node.set_enabled(False)
            return True

        for child in checked_node.get_children():
            if self._search_parent(child, orphan_node):
                return True
        return False

    def node_to_data_list(self, node: DataNode) -> List[Data]:
        """
        Extracts data from DataNodes into list
        :param node: DataNode for extracting
        :return: list of Data
        """
        return self._to_data_list(node, [])

    def node_list_to_data_list(self, nodes: List[DataNode]) -> List[Data]:
        """
        Extracts data from DataNodes list into list
        :param nodes: DataNode list for extracting
        :return: list of Data
        """
        result = []
        for node in nodes:
            result.extend(self.node_to_data_list(node))
        return result

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

    def node_list_has_data(self, node_list: List[DataNode], data: Data) -> bool:
        """
        Checks if any node in list has selected data
        :param node_list: list of DataNodes for checking
        :param data: searched data
        :return: True if Node with selected data present in list
        """
        for node in node_list:
            if node.has(data):
                return True
        return False

    def update_node_list_with_data_list(self, nodes_list, data_list, append_new=True) -> None:
        """
        Method for applying update for used nodes.
        Applies value changing, delete effect. Also new elements will be appended to the tree.
        :param nodes_list: list of nodes for updating
        :param data_list: update data
        :param append_new: enabled by default, appends new nodes from data_list.
                           Disable when just update required.
        :return: None
        """
        # reserving list for removing from it updated elements
        process_list = data_list[:]
        for node in nodes_list:
            self._update_node_with_data_list(node, process_list)

        if append_new:
            nodes_list.extend([DataNode(instance=a) for a in process_list])
            self.update_node_hierarchy(nodes_list, remove_from_list=True)

    def _update_node_with_data_list(self, node: DataNode, data_list: List[Data]) -> None:
        """
        Private method providing existed nodes update with passed list of data
        :param node: node for update
        :param data_list: list of update data
        :return: None
        """
        i = 0
        while i < len(data_list):
            data = data_list[i]
            if self._update_node_with_data(node, data):
                data_list.remove(data)
            else:
                i += 1

    def _update_node_with_data(self, node: DataNode, data: Data) -> bool:
        """
        Private method for attempting update node with data.
        Returns True if attempt was successfull.
        :param node: node for update
        :param data: update data
        :return: True if node successfully update
        """
        if node == data:
            node.set_value(data.get_value())
            if not data.is_enabled():
                node.set_enabled(False)
            return True
        else:
            for child in node.get_children():
                if self._update_node_with_data(child, data):
                    return True
        return False

    def node_list_to_json(self, encoder: DataEncoder, data_nodes: List[DataNode]):
        data_list = self.node_list_to_data_list(data_nodes)
        return encoder.encode(data_list)
