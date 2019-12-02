#!/bin/python3
# -*- coding: utf-8 -*-

import sys
from typing import List

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from data_node import DataNode
from data import Data
from data_serializer import DataEncoder
from data_serializer import DataDecoder
from data_controller import DataNodeController


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tree_db = None
        self.tree_cache = None
        self.data_db = []
        self.data_cache = []

        self._data_controller = DataNodeController()
        self._data_decoder = DataDecoder()
        self._data_encoder = DataEncoder()
        self.init_ui()

    def init_ui(self) -> None:
        # initializing layouts
        layout_main = QVBoxLayout()
        layout_tree_panel = QHBoxLayout()
        layout_db_tree = QVBoxLayout()
        layout_cache_tree = QVBoxLayout()
        layout_cache_actions = QHBoxLayout()
        layout_db_actions = QHBoxLayout()

        widget_central = QWidget()
        widget_central.setLayout(layout_main)
        self.setCentralWidget(widget_central)

        # initializing components
        self.tree_db = QTreeView(self)
        self.tree_cache = QTreeView(self)

        label_db_tree = QLabel("Database Tree", self)
        label_cache_tree = QLabel("Cache Tree", self)
        button_to_cache = QPushButton(">>>", self)
        button_new_element = QPushButton("New", self)
        button_delete_element = QPushButton("Delete", self)
        button_edit_element = QPushButton("Edit", self)
        button_apply_cache = QPushButton("Apply", self)
        button_reset = QPushButton("Reset", self)

        # put elements to layouts
        layout_main.addLayout(layout_tree_panel)
        layout_tree_panel.addLayout(layout_db_tree)
        layout_tree_panel.addWidget(button_to_cache)
        layout_tree_panel.addLayout(layout_cache_tree)
        layout_db_tree.addWidget(label_db_tree)
        layout_db_tree.addWidget(self.tree_db)
        layout_db_tree.addLayout(layout_db_actions)
        layout_cache_tree.addWidget(label_cache_tree)
        layout_cache_tree.addWidget(self.tree_cache)
        layout_cache_tree.addLayout(layout_cache_actions)
        layout_cache_actions.addWidget(button_new_element)
        layout_cache_actions.addWidget(button_edit_element)
        layout_cache_actions.addWidget(button_delete_element)
        layout_db_actions.addWidget(button_apply_cache)
        layout_db_actions.addWidget(button_reset)

        # configure elements
        self.data_db = [self.create_data_sample()]
        self.tree_db.header().hide()
        self.sync_tree_db()

        self.data_cache = []
        self.tree_cache.header().hide()
        self.tree_cache.setModel(QStandardItemModel())

        # slot-sognal connecting
        button_to_cache.clicked.connect(self.add_item_to_cache)
        button_delete_element.clicked.connect(self.delete_item)
        button_edit_element.clicked.connect(self.edit_item)
        button_new_element.clicked.connect(self.add_item)
        button_reset.clicked.connect(self.reset)
        button_apply_cache.clicked.connect(self.apply_cache_changes)

        widget_central.setMinimumHeight(700)
        self.show()

    def sync_tree_with_data(self, tree: QTreeView, data: List[DataNode]) -> None:
        """
        Executes synchronization between DataNode and StandardItemModel.
        Updates tree view.
        :param tree: TreeView for updating
        :param data: list of DataNodes for update
        :return:
        """
        tree.setModel(self.create_model_from_nodes(data))
        tree.expandAll()

    def sync_tree_db(self) -> None:
        """
        Shortcut for sync Database Tree
        :return: None
        """
        self.sync_tree_with_data(self.tree_db, self.data_db)

    def sync_tree_cache(self) -> None:
        """
        Shortcut for sync Cache Tree
        :return: None
        """
        self.sync_tree_with_data(self.tree_cache, self.data_cache)

    def get_selected_item(self, tree: QTreeView) -> QStandardItem:
        """
        Shortcut for receiving current selected element in tree
        :param tree: QTreeView for requesting selected element
        :return: QStandardItem reference, None if no selection available
        """
        index = tree.currentIndex()
        return tree.model().itemFromIndex(index)

    def add_item_to_cache(self) -> None:
        """
        Appends selected element it database tree to cache tree.
        Converts selected database item data to json and sends it to the cache
        :return: None
        """
        item = self.get_selected_item(self.tree_db)
        if item is None:
            return

        data_node = item.data()
        json_cache = self._data_encoder.encode(data_node.get_instance())
        self.send_data_to_cache(json_cache)

    def send_data_to_cache(self, json_data: str) -> None:
        """
        Decodes data from json into Data,
        then appends it to the cache.
        If cache already has that element, nothing will be appended.
        :param json_data: received json format data
        :return: None
        """
        data = self._data_decoder.decode(json_data)
        if not self._data_controller.node_list_has_data(self.data_cache, data):
            self.data_cache.append(DataNode(instance=data))
            self._data_controller.update_node_hierarchy(self.data_cache, remove_from_list=True)
            self.sync_tree_cache()

    def delete_item(self) -> None:
        """
        Delete selected cache item (disables it).
        If no item was selected, nothing will happens.
        :return: None
        """
        item = self.get_selected_item(self.tree_cache)
        if item is None:
            return

        item.data().set_enabled(False)
        self.sync_tree_cache()

    def edit_item(self) -> None:
        """
        Show edit window for selected cache item.
        IF no item was selected, nothing will happens
        :return: None
        """
        item = self.get_selected_item(self.tree_cache)
        if item is None:
            return

        text, ok = QInputDialog.getText(self, "Edit data", "Data:", text=item.data().get_value())
        if ok:
            item.setText(text)
            item.data().set_value(text)

    def add_item(self) -> None:
        """
        Show new element window for selected cache item.
        IF no item was selected, nothing will happens
        :return: None
        """
        item = self.get_selected_item(self.tree_cache)
        if item is None:
            return

        text, ok = QInputDialog.getText(self, "Appending new data", "Data:")
        if ok:
            parent_id = item.data().get_id()
            data = Data(text, parent_id)
            data_node = DataNode(instance=data)
            self.data_cache.append(data_node)
            self._data_controller.update_node_hierarchy(self.data_cache, remove_from_list=True)
            self.sync_tree_cache()

    def apply_cache_changes(self) -> None:
        """
        Converts cache data then sends it to the database.
        :return: None
        """
        json_data_cache = self._data_controller.node_list_to_json(self._data_encoder, self.data_cache)
        self.send_cache_changes(json_data_cache)

    def send_cache_changes(self, json_data: str) -> None:
        """
        Converts received json data to Data list,
        then updates Database with that list. Tree updated.
        Also cache sync provided.
        :param json_data: update for database in json format
        :return: None
        """
        data_list = self._data_decoder.decode(json_data)
        self._data_controller.update_node_list_with_data_list(self.data_db, data_list)
        self.sync_tree_db()

        # There are possible updates which touch any cache data, so updating cache data
        json_data_db = self._data_controller.node_list_to_json(self._data_encoder, self.data_db)
        self.update_cache(json_data_db)

    def update_cache(self, json_data: str) -> None:
        """
        Updates cache data with json from Database data.
        :param json_data: jsonned Data from Database
        :return: None
        """
        data_list = self._data_decoder.decode(json_data)
        self._data_controller.update_node_list_with_data_list(nodes_list=self.data_cache,
                                                              data_list=data_list,
                                                              append_new=False)
        self.sync_tree_cache()

    def create_model_from_nodes(self, nodes: List[DataNode]) -> QStandardItemModel:
        """
        Shortcut for create model with data from DataNode
        :param nodes: data source
        :return: result QStandardItemModel
        """
        model = QStandardItemModel()
        for node in nodes:
            model.appendRow(self.node_to_item(node))
        return model

    def node_to_item(self, node: DataNode) -> QStandardItem:
        """
        Create QStandardItem based on DataNode.
        :param node: data source node
        :return: QStandardItem with node data
        """
        item = QStandardItem(node.get_value())
        item.setData(node)
        item.setEnabled(node.is_enabled())
        item.setEditable(False)
        for child in node.get_children():
            item.appendRow(self.node_to_item(child))
        return item

    def reset(self) -> None:
        """
        Reset all states.
        :return: None
        """
        self.data_cache = []
        self.data_db = [self.create_data_sample()]
        self.sync_tree_db()
        self.sync_tree_cache()

    def create_data_sample(self) -> DataNode:
        """
        Create start sample structure
        :return: root DataNode
        """
        root = DataNode("Grandpa")

        node1 = DataNode("Node1", parent=root)
        node2 = DataNode("Node2", parent=root)
        node3 = DataNode("Node3", parent=root)

        child1_1 = DataNode("Child1_1", parent=node1)
        child1_2 = DataNode("Child1_2", parent=node1)

        child2_1 = DataNode("Child2_1", parent=node2)
        child2_2 = DataNode("Child2_2", parent=node2)
        child2_3 = DataNode("Child2_3", parent=node2)

        child3_1 = DataNode("Child3_1", parent=node3)

        grandchild1_1_1 = DataNode("Grandchild1_1_1", parent=child1_1)
        grandchild1_1_2 = DataNode("Grandchild1_1_2", parent=child1_1)

        grandchild1_2_1 = DataNode("Grandchild1_2_1", parent=child1_2)

        grandchild2_1_1 = DataNode("Grandchild2_1_1", parent=child2_1)
        grandchild2_1_2 = DataNode("Grandchild2_1_2", parent=child2_1)
        grandchild2_1_3 = DataNode("Grandchild2_1_3", parent=child2_1)

        grandchild2_2_1 = DataNode("Grandchild2_2_1", parent=child2_2)
        grandchild2_2_2 = DataNode("Grandchild2_2_2", parent=child2_2)

        grandchild2_3_1 = DataNode("Grandchild2_3_1", parent=child2_3)
        grandchild2_3_2 = DataNode("Grandchild2_3_2", parent=child2_3)
        grandchild2_3_3 = DataNode("Grandchild2_3_3", parent=child2_3)
        grandchild2_3_4 = DataNode("Grandchild2_3_4", parent=child2_3)

        grandchild3_1_1 = DataNode("Grandchild3_1_1", parent=child3_1)
        grandchild3_1_2 = DataNode("Grandchild3_1_2", parent=child3_1)
        grandchild3_1_3 = DataNode("Grandchild3_1_3", parent=child3_1)
        grandchild3_1_4 = DataNode("Grandchild3_1_4", parent=child3_1)
        grandchild3_1_5 = DataNode("Grandchild3_1_5", parent=child3_1)

        return root


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Cached Database")
    window = MainWindow()
    sys.exit(app.exec_())
