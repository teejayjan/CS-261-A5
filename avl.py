# Course: CS261 - Data Structures
# Author: Timothy Jan
# Assignment: 5
# Description: Implements AVL Tree.

import random

from bst import BST
from bst import TreeNode
from bst import Stack
from bst import Queue


def check_pointers(tree) -> bool:
    """
    Perform pre-order traversal of the tree
    Return False if found any problems with pointers
    """
    s = Stack()
    s.push(tree.root)
    while not s.is_empty():
        node = s.pop()
        if node:
            # check for correct height (relative to children)
            l = node.left.height if node.left else -1
            r = node.right.height if node.right else -1
            if node.height != 1 + max(l, r):
                return False

            if node.parent:
                # parent and child pointers are in sync
                if node.value < node.parent.value:
                    check_node = node.parent.left
                else:
                    check_node = node.parent.right
                if check_node is not node:
                    return False
            else:
                # NULL parent is only allowed on the root of the tree
                if node != tree.root:
                    return False

            s.push(node.right)
            s.push(node.left)
    return True

class AVLTreeNode(TreeNode):
    """
    AVL Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        super().__init__(value)
        self.parent = None
        self.height = 0


class AVL(BST):
    def add(self, value):
        """Adds a new value to the tree, maintaining AVL property. Does not allow addition of duplicate values."""

        def rec_add(node):
            # root node
            if node is None:
                self.root = AVLTreeNode(value)
                return self.root
            # exit if we've hit a duplicate
            if value == node.value:
                return None
            # left
            elif value < node.value:
                if node.left is not None:
                    return rec_add(node.left)
                elif node.left is None and value < node.value:
                    new_node = AVLTreeNode(value)
                    node.left = new_node
                    new_node.parent = node
                    return new_node
            # right
            elif value >= node.value:
                if node.right is not None:
                    return rec_add(node.right)
                elif node.right is None and value >= node.value:
                    new_node = AVLTreeNode(value)
                    node.right = new_node
                    new_node.parent = node
                    return new_node

        new_node = rec_add(self.root)
        if new_node is None:  # exit if new node was a duplicate (and therefore wasn't added)
            return
        parent = new_node.parent
        while parent is not None:
            self.rebalance(parent)
            parent = parent.parent

    def remove(self, value) -> bool:
        """Removes the first instance of specified value from the AVL tree. Returns True if the value was removed,
        otherwise returns False."""

        # EMPTY TREE
        if self.root is None:
            return False

        parent = self.remove_helper(value)
        # removed node, but no need to rebalance
        if parent is None:
            return True
        # couldn't find node
        elif parent is False:
            return False
        # otherwise, we got a parent node back and need to rebalance
        while parent is not None:
            self.rebalance(parent)
            parent = parent.parent
        return True

    def remove_helper(self, value):
        """Helper function to remove specified value. Returns removed node's parent, None if removed node doesn't
        have a parent, or False if specified value doesn't exist in the tree."""

        def rec_successor(node):
            if node.left is None:
                s_and_ps.enqueue(node)
                return
            s_and_ps.dequeue()
            s_and_ps.enqueue(node)
            return rec_successor(node.left)

        def rec_contains(node):
            if node is None:
                return False
            elif value < node.value:
                n_and_pn.push(node)
                if value == node.value:
                    return True
                else:
                    return rec_contains(node.left)
            elif value >= node.value:
                n_and_pn.push(node)
                if value == node.value:
                    return True
                else:
                    return rec_contains(node.right)

        # REMOVING ROOT
        if value == self.root.value:
            # root has no children
            if self.root.left is None and self.root.right is None:
                self.root = None
                return None
            # root has one child
            elif self.root.left is not None and self.root.right is None or \
                    self.root.left is None and self.root.right is not None:
                # child is on left
                if self.root.right is None:
                    self.root = self.root.left
                    self.root.parent = None
                    return None
                # child is on the right
                else:
                    self.root = self.root.right
                    self.root.parent = None
                    return None
            # root has two children, find successor
            else:
                s_and_ps = Queue()
                s_and_ps.enqueue(self.root)
                rec_successor(self.root.right)

                parent_successor = s_and_ps.dequeue()
                successor = s_and_ps.dequeue()

                # successor is root's right child
                if self.root.right is successor:
                    successor.left = self.root.left
                    if self.root.left is not None:
                        self.root.left.parent = successor
                    self.root = successor
                    self.root.parent = None
                    return self.root

                else:  # successor is not adjacent to root
                    # if S has a right child, assign it as PS's left child
                    if successor.right is not None:
                        parent_successor.left = successor.right
                        parent_successor.left.parent = parent_successor
                    if parent_successor.left is successor:
                        parent_successor.left = None
                    # update L/R pointers
                    successor.left = self.root.left
                    successor.right = self.root.right
                    # update parent pointers
                    if self.root.left is not None:
                        self.root.left.parent = successor
                    if self.root.right is not None:
                        self.root.right.parent = successor
                    self.root = successor
                    self.root.parent = None
                    # self.update_height(parent_successor)
                    return parent_successor

        # VALUE IS NOT THE ROOT
        # check if value is in the tree, and if so, save node to be removed and its parent
        n_and_pn = Stack()
        result = rec_contains(self.root)
        if result is False:  # contains returned False, so return False to remove()
            return False

        node = n_and_pn.pop()
        parent_node = n_and_pn.pop()

        # NODE HAS NO CHILDREN
        if node.left is None and node.right is None:
            if parent_node.left is node:
                parent_node.left = None
                return parent_node
            else:
                parent_node.right = None
                return parent_node
        # NODE HAS ONE CHILD
        elif node.left is not None and node.right is None or node.left is None and node.right is not None:
            if parent_node.left is node:  # node is parent's left child
                if node.right is None:  # node has a left child
                    parent_node.left = node.left
                    parent_node.left.parent = parent_node
                    return parent_node
                else:  # node has a right child
                    parent_node.left = node.right
                    parent_node.left.parent = parent_node
                    return parent_node
            else:  # node is parent's right child
                if node.right is None:  # node has a left child
                    parent_node.right = node.left
                    parent_node.right.parent = parent_node
                    return parent_node
                else:  # node has a right child
                    parent_node.right = node.right
                    parent_node.right.parent = parent_node
                    return parent_node
        # NODE HAS TWO CHILDREN
        else:
            s_and_ps = Queue()
            s_and_ps.enqueue(node)
            rec_successor(node.right)

            parent_successor = s_and_ps.dequeue()
            successor = s_and_ps.dequeue()

            # N's left child becomes S's left child
            successor.left = node.left
            successor.left.parent = successor

            # S is not N's right child
            if successor is not node.right:
                # S's right child (could be None) becomes PS's left child
                parent_successor.left = successor.right
                if parent_successor.left is not None:
                    parent_successor.left.parent = parent_successor
                # N's right child becomes S's right child
                successor.right = node.right
                successor.right.parent = successor

            # Update PN pointers to S
            if parent_node.left is node:  # node was parent node's left child
                parent_node.left = successor
                successor.parent = parent_node
                self.update_height(parent_successor)
                return successor
            else:  # node was parent node's right child
                parent_node.right = successor
                successor.parent = parent_node
                self.update_height(parent_successor)
                return successor


    def rebalance(self, node):
        """Rebalances AVL tree around specified node."""
        if self.balance_factor(node) < -1:
            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
                node.left.parent = node
            node_parent = node.parent  # save node parent in case it's overwritten in rotate
            new_root = self.rotate_right(node)
            new_root.parent = node_parent
            # node was former root (and therefore has no parent)
            if node_parent is None:
                self.root = new_root
            # old node parent exists
            elif node_parent is not None:
                # node was node_parent's left child
                if node_parent.left is node:
                    node_parent.left = new_root
                # else, node node_parent's right child
                else:
                    node_parent.right = new_root
        elif self.balance_factor(node) > 1:
            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
                node.right.parent = node
            node_parent = node.parent  # save node parent in case it's overwritten in rotate
            new_root = self.rotate_left(node)
            new_root.parent = node_parent
            # node was former root (and therefore has no parent)
            if node_parent is None:
                self.root = new_root
            # old node parent exists
            elif node_parent is not None:
                # node was node_parent's left child
                if node_parent.left is node:
                    node_parent.left = new_root
                # else, node node_parent's right child
                else:
                    node_parent.right = new_root
        else:
            self.update_height(node)

    def rotate_left(self, node):
        """Rotates AVL left around specified node."""
        child = node.right
        node.right = child.left
        if node.right is not None:
            node.right.parent = node
        child.left = node
        child.left.parent = child
        self.update_height(node)
        self.update_height(child)
        return child

    def rotate_right(self, node):
        """Rotates AVL right around specified node."""
        child = node.left
        node.left = child.right
        if node.left is not None:
            node.left.parent = node
        child.right = node
        child.right.parent = child
        self.update_height(node)
        self.update_height(child)
        return child

    def update_height(self, node):
        l = node.left.height if node.left else -1
        r = node.right.height if node.right else -1
        node.height = max(l, r) + 1

    def balance_factor(self, node):
        """Returns the balance factor at specified node."""
        l = node.left.height if node.left else - 1
        r = node.right.height if node.right else -1
        return r - l


if __name__ == '__main__':

    # print("\nPDF - method add() example 1")
    # print("----------------------------")
    # test_cases = (
    #     (1, 2, 3),          #RR
    #     (3, 2, 1),          #LL
    #     (1, 3, 2),          #RL
    #     (3, 1, 2),          #LR
    # )
    # for case in test_cases:
    #     avl = AVL(case)
    #     print(avl)
    #
    #
    # print("\nPDF - method add() example 2")
    # print("----------------------------")
    # test_cases = (
    #     (10, 20, 30, 40, 50),   # RR, RR
    #     (10, 30, 30, 50, 40),   # RR, RL
    #     (30, 20, 10, 5, 1),     # LL, LL
    #     (30, 20, 10, 1, 5),     # LL, LR
    #     (5, 4, 6, 3, 7, 2, 8),  # LL, RR
    #     (range(0, 30, 3)),
    #     (range(0, 31, 3)),
    #     (range(0, 34, 3)),
    #     (range(10, -10, -2)),
    #     ('A', 'B', 'C', 'D', 'E'),
    #     (1, 1, 1, 1),
    # )
    # for case in test_cases:
    #     avl = AVL(case)
    #     print('INPUT  :', case)
    #     print('RESULT :', avl)

    # print("\nCustom - method remove() example A")  # try to remove a value not in the tree
    # print("-------------------------------")
    # avl = AVL([1, 2, 3, 4, 5])
    # avl.remove(7)
    # print("Result: ", avl)
    #
    # print("\nCustom - method remove() example B")
    # print("-------------------------------")
    # avl = AVL([-59653, -64452, 25849, 4112, 57293, 78134, 71381, 37385])
    # print("Before Remove: ", avl.post_order_traversal())
    # avl.remove(4112)
    # print("Expected: ", [-64452, 25849, -59653, 57293, 78134, 71381, 37385])
    # print("Result: ", avl.post_order_traversal())
    #
    #
    # print("\nCustom - method remove() example C")
    # print("-------------------------------")
    # avl = AVL(
    #     [-90394, -71765, -86392, -56202, -45261, 4375, 8574, 6893, -3887, -69120, 11146, 34893, 33637, 47112, 71476,
    #      93218, 74461, 54189, 45310, 9220
    #      ])
    # print("Before Remove: ", avl.post_order_traversal())
    # avl.remove(-69120)
    # print("Expected: ", [-90394, -71765, -86392, -45261, 4375, 8574, 6893, -3887, -56202, 11146, 34893, 33637, 47112,
    #                      71476, 93218, 74461, 54189, 45310, 9220])
    # print("Result: ", avl.post_order_traversal())

    # print("\nCustom - method remove() example D")
    # print("-------------------------------")
    # avl = AVL([-13218, -75324, -86453, -92015, -76860, -83841, -64793, -58968, 23178, -3646, -3787, 11741, 80118, 78541,
    #            61334, 91055, 90651, 93659])
    # print("TREE pre order: ", avl.pre_order_traversal())
    # print("TREE post order: ", avl.post_order_traversal())
    # avl.remove(-75324)
    # print("EXPECTED pre order: ", [-13218, -76860, -86453, -92015, -83841, -64793, -58968, 23178, -3646, -3787, 11741,
    #                                80118, 78541, 61334, 91055, 90651, 93659])
    # print("EXPECTED post order: ", [-92015, -83841, -86453, -58968, -64793, -76860, -3787, 11741, -3646, 61334, 78541,
    #                                 90651, 93659, 91055, 80118, 23178, -13218])
    # print("RESULT pre order: ", avl.pre_order_traversal())
    # print("RESULT post order: ", avl.post_order_traversal())

    # print("\nCustom - method remove() example E")
    # print("-------------------------------")
    # nodes = [61926, -21076, -47614, -72156, -24709, 50499, 8188, 89737, 68841, 94899]
    # avl = AVL(nodes)
    # # for node in nodes:
    # #     avl.add(node)
    # print("Before removal: ", avl.post_order_traversal())
    # avl.remove(-47614)
    # print("Expected: ", [-72156, -24709, 8188, 50499, -21076, 68841, 94899, 89737, 61926])
    # print("Result: post order", avl.post_order_traversal())

    # print("\nCustom - method remove() example F")
    # print("-------------------------------")
    # nodes = [-29302, -81149, -98516, -35909, -71588, 52443, 32164, -1459, 81196, 69041]
    # avl = AVL()
    # for node in nodes:
    #     avl.add(node)
    # print("Before Removal: ", avl.pre_order_traversal())
    # avl.remove(-81149)
    # print("Expected pre-order: ", [-29302, -71588, -98516, -35909, 52443, 32164, -1459, 81196, 69041])
    # print("Result pre-order: ", avl.pre_order_traversal())

    #
    # print("\nPDF - method remove() example 1")
    # print("-------------------------------")
    # test_cases = (
    #     ((1, 2, 3), 1),  # no AVL rotation
    #     ((1, 2, 3), 2),  # no AVL rotation
    #     ((1, 2, 3), 3),  # no AVL rotation
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 0),
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    # )
    # for tree, del_value in test_cases:
    #     avl = AVL(tree)
    #     print('INPUT  :', avl, "DEL:", del_value)
    #     avl.remove(del_value)
    #     print('RESULT :', avl)
    #
    # print("\nPDF - method remove() example 2")
    # print("-------------------------------")
    # test_cases = (
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
    #     ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
    #     ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
    #     ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    # )
    # for tree, del_value in test_cases:
    #     avl = AVL(tree)
    #     print('INPUT  :', avl, "DEL:", del_value)
    #     avl.remove(del_value)
    #     print('RESULT :', avl)
    #     # print(check_pointers(avl))
    #
    # print("\nPDF - method remove() example 3")
    # print("-------------------------------")
    # case = range(-9, 16, 2)
    # avl = AVL(case)
    # for del_value in case:
    #     print('INPUT  :', avl, del_value)
    #     avl.remove(del_value)
    #     print('RESULT :', avl)
    #     # print(check_pointers(avl))
    #
    # print("\nPDF - method remove() example 4")
    # print("-------------------------------")
    # case = range(0, 34, 3)
    # avl = AVL(case)
    # for _ in case[:-2]:
    #     print('INPUT  :', avl.size(), avl, avl.root)
    #     avl.remove(avl.root.value)
    #     print('RESULT :', avl)
    #     # print(check_pointers(avl))

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL(case)
        if avl.size() != len(case):
            raise Exception("PROBLEM WITH ADD OPERATION")
        for value in case[::2]:
            avl.remove(value)
        if avl.size() != len(case) - len(case[::2]):
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('Stress test finished')
    print(check_pointers(avl))

    # """ Comprehensive example 1 """
    # print("\nComprehensive example 1")
    # print("-----------------------")
    # tree = AVL()
    # header = 'Value   Size  Height   Leaves   Unique   '
    # header += 'Complete?  Full?    Perfect?'
    # print(header)
    # print('-' * len(header))
    # print(f'  N/A {tree.size():6} {tree.height():7} ',
    #       f'{tree.count_leaves():7} {tree.count_unique():8}  ',
    #       f'{str(tree.is_complete()):10}',
    #       f'{str(tree.is_full()):7} ',
    #       f'{str(tree.is_perfect())}')
    #
    # for value in [10, 5, 3, 15, 12, 8, 20, 1, 4, 9, 7]:
    #     tree.add(value)
    #     print(f'{value:5} {tree.size():6} {tree.height():7} ',
    #           f'{tree.count_leaves():7} {tree.count_unique():8}  ',
    #           f'{str(tree.is_complete()):10}',
    #           f'{str(tree.is_full()):7} ',
    #           f'{str(tree.is_perfect())}')
    # print()
    # print(tree.pre_order_traversal())
    # print(tree.in_order_traversal())
    # print(tree.post_order_traversal())
    # print(tree.by_level_traversal())
    #
    # """ Comprehensive example 2 """
    # print("\nComprehensive example 2")
    # print("-----------------------")
    # tree = AVL()
    # header = 'Value   Size  Height   Leaves   Unique   '
    # header += 'Complete?  Full?    Perfect?'
    # print(header)
    # print('-' * len(header))
    # print(f'N/A   {tree.size():6} {tree.height():7} ',
    #       f'{tree.count_leaves():7} {tree.count_unique():8}  ',
    #       f'{str(tree.is_complete()):10}',
    #       f'{str(tree.is_full()):7} ',
    #       f'{str(tree.is_perfect())}')
    #
    # for value in 'DATA STRUCTURES':
    #     tree.add(value)
    #     print(f'{value:5} {tree.size():6} {tree.height():7} ',
    #           f'{tree.count_leaves():7} {tree.count_unique():8}  ',
    #           f'{str(tree.is_complete()):10}',
    #           f'{str(tree.is_full()):7} ',
    #           f'{str(tree.is_perfect())}')
    # print('', tree.pre_order_traversal(), tree.in_order_traversal(),
    #       tree.post_order_traversal(), tree.by_level_traversal(),
    #       sep='\n')

    # case = (29454, -25678, 84629, -70250, 71956, 59994, 84629, 99144)
    # avl = AVL(case)
    # print(avl, check_pointers(avl))
    # avl.remove(71956)
    # print(avl, check_pointers(avl))

    nodes = (-8758, -45270, -57966, -64587, -30086, -31755, -16307, -12775, 56127, 37783, 10369, 44151, 65732, 61396, 63016, 88922)
    avl = AVL()
    for node in nodes:
        avl.add(node)
    print("Before: ", avl.pre_order_traversal())
    avl.remove(-45270)
    print("After: ", avl.pre_order_traversal())
    print("returning successor: ", [-12775, -31755, -57966, -64587, -30086, -16307, 37783, -8758, 10369, 63016, 56127, 44151, 61396, 65732, 88922])
