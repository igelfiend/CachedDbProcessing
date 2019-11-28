import unittest
from data_node import DataNode
from data_node import DataNodeException, DataNodeInstanceException
from copy import deepcopy


class TestDataNodeInit(unittest.TestCase):
    """
    Test cases for initing NodeData
    """
    def test_with_only_value(self):
        try:
            node_value = "TestNode"
            node = DataNode(node_value)

            self.assertEqual(node.get_value() == node_value, True,
                             "TestInit: test with value case: "
                             "value set incorrectly")
            self.assertIsNone(node.get_parent_id(),
                              "TestInit: test with value case: "
                              "parent must be None")
            self.assertIsNotNone(node.get_id(),
                                 "TestInit: test with value case: "
                                 "id of the node was not set")
        except DataNodeInstanceException:
            self.assertTrue(False,
                            "TestInit: test with value case: "
                            "exception must not be raised")

    def test_with_correct_parent(self):
        try:
            grand_node_value = "Grand"
            grand_node = DataNode(grand_node_value)

            node1_value = "TestNode1"
            node2_value = "TestNode2"
            node1 = DataNode(node1_value, parent=grand_node)
            node2 = DataNode(node2_value, parent=grand_node)

            node1_child1_value = "Node1Child1"
            node1_child2_value = "Node1Child2"
            node1_child3_value = "Node1Child3"
            node1_child1 = DataNode(node1_child1_value, parent=node1)
            node1_child2 = DataNode(node1_child2_value, parent=node1)
            node1_child3 = DataNode(node1_child3_value, parent=node1)

            self.assertIsNone(grand_node.get_parent_id(),
                              "TestInit: test with correct parent: "
                              "root node parent must be None")
            self.assertEqual(node1.get_parent_id(), grand_node.get_id(),
                             "TestInit: test with correct parent: "
                             "root node must be parent of the node1")
            self.assertEqual(node2.get_parent_id(), grand_node.get_id(),
                             "TestInit: test with correct parent: "
                             "root node must be parent of the node2")
            self.assertEqual(node1_child1.get_parent_id(), node1.get_id(),
                             "TestInit: test with correct parent: "
                             "node1 must be parent of the child1")
            self.assertEqual(node1_child2.get_parent_id(), node1.get_id(),
                             "TestInit: test with correct parent: "
                             "node1 must be parent of the child2")
            self.assertEqual(node1_child2.get_parent_id(), node1.get_id(),
                             "TestInit: test with correct parent: "
                             "node1 must be parent of the child3")
        except DataNodeInstanceException:
            self.assertTrue(False,
                            "TestInit: exception was raised")

    def test_with_incorrect_parent_instance(self):
        try:
            grand_node_value = "Grand"
            grand_node = DataNode(grand_node_value)

            node1_value = "TestNode1"
            node2_value = "TestNode2"
            node1 = DataNode(node1_value, parent=grand_node)
            node2 = DataNode(node2_value, parent=grand_node_value)

            self.assertTrue(False,
                            "TestInit: Exception must be raised")
        except DataNodeInstanceException:
            pass


class TestDataNodeEquals(unittest.TestCase):
    """
    Test cases for applying equal operator in DataNode
    """
    def test_with_self(self):
        node1 = DataNode("TestNode")
        self.assertTrue(node1 == node1,
                        "TestEqual: test with self: "
                        "must be equal with self")
        self.assertFalse(node1 != node1,
                         "TestEqual: test with self: "
                         "result of not equal operator must be false")

    def test_with_copy(self):
        node1 = DataNode("TestNode")
        node1_copy = deepcopy(node1)
        self.assertTrue(node1 == node1_copy,
                        "TestEqual: test with copy: "
                        "node with it copy must be equal")
        self.assertFalse(node1 != node1_copy,
                         "TestEqual: test with copy: "
                         "result of not equal operator must be false")

    def test_with_same_value(self):
        node_value = "TestNode"
        node1 = DataNode(node_value)
        node2 = DataNode(node_value)
        self.assertFalse(node1 == node2,
                         "TestEqual: test with same value: "
                         "nodes must not be equal")
        self.assertTrue(node1 != node2,
                        "TestEqual: test with same value: "
                        "not equal operator must be true")

    def test_with_diff_value(self):
        node1 = DataNode("TestNode1")
        node2 = DataNode("TestNode2")
        self.assertFalse(node1 == node2,
                         "TestEqual: test with diff values: "
                         "nodes must not be equal")
        self.assertTrue(node1 != node2,
                        "TestEqual: test with diff values: "
                        "not equal operator must be true")

    def test_with_not_instance(self):
        node1_value = "TestNode1"
        node1 = DataNode(node1_value)
        self.assertFalse(node1 == node1_value,
                         "TestEqual: test with not instance: "
                         "eq with not instance must be false")


class TestDataNodeChildAppending(unittest.TestCase):
    """
    Test cases for appending children elements
    """
    def test_append_first_child(self):
        node = DataNode("TestNode")
        child = DataNode("ChildNode")

        try:
            node.append_child(child)
            self.assertTrue(len(node.get_children()) == 1,
                            "TestAppend: test appending first element: "
                            "Children list has not single element")
            self.assertTrue(child in node.get_children(),
                            "TestAppend: test appending first element: "
                            "Different element created in children list")
        except DataNodeInstanceException:
            self.assertTrue(False,
                            "TestAppend: test appending first element: "
                            "Exception must not be raised")

    def test_append_multiple_children(self):
        node = DataNode("TestNode")
        child1 = DataNode("ChildNode1")
        child2 = DataNode("ChildNode2")
        child3 = DataNode("ChildNode3")

        try:
            node.append_child(child1)
            node.append_child(child2)
            node.append_child(child3)
            self.assertTrue(len(node.get_children()) == 3,
                            "TestAppend: test appending multiple children: "
                            "Incorrect count of the appended elements")
            self.assertTrue(child1 in node.get_children(),
                            "TestAppend: test appending multiple children: "
                            "Different element instead child 1 created in children list")
            self.assertTrue(child2 in node.get_children(),
                            "TestAppend: test appending multiple children: "
                            "Different element instead child 2 created in children list")
            self.assertTrue(child3 in node.get_children(),
                            "TestAppend: test appending multiple children: "
                            "Different element instead child 3 created in children list")
        except DataNodeInstanceException:
            self.assertTrue(False,
                            "TestAppend: test appending first element: "
                            "Exception must not be raised")

    def test_append_incorrect_instance(self):
        node = DataNode("TestNode")
        child_value = "ChildNode"
        child = DataNode(child_value)

        try:
            node.append_child(child_value)
            self.assertTrue(False,
                            "TestAppend: test incorrect instance appending: "
                            "Exception must be raised")
        except DataNodeInstanceException:
            pass


if __name__ == '__main__':
    unittest.main()
