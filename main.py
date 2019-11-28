#!/bin/python
# -*- coding: utf-8 -*-

from data_node import DataNode
from data_serializer import DataEncoder
from data_serializer import DataDecoder
from data_controller import DataNodeController


def create_data_sample() -> DataNode:
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
    return root


def main():
    encoder = DataEncoder(indent=4)
    decoder = DataDecoder()
    controller = DataNodeController()

    data = create_data_sample()

    raw = controller.to_data_list(data)

    print("initial data struct:")
    print(repr(raw))
    #
    # json_data = encoder.encode(raw)
    # print("jsonned data")
    # print(json_data)
    #
    # print("processing backward")
    # upd_data = decoder.decode(json_data)
    # print(repr(upd_data))

    print("generate tree")
    upd_data = controller.create_node_hierarchy(raw)
    print(repr(upd_data[0]))


if __name__ == "__main__":
    main()
