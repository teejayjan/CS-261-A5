# Course: CS261 - Data Structures
# Author: Timothy Jan
# Assignment: 5
# Description: Implements AVL Tree.

import random

from bst import BST
from bst import TreeNode
from bst import Stack
from bst import Queue


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

        parent = self.remove_helper(value)
        if parent is False:
            return False
        if parent is not None:
            while parent is not None:
                self.rebalance(parent)
                parent = parent.parent
            return True
        # remove helper returns None, which means there is no parent node with which to rotate/balance
        else:
            return True

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
            if node_parent is not None:
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
            if node_parent is not None:
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
        node.parent = child
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
        node.parent = child
        self.update_height(node)
        self.update_height(child)
        return child

    def remove_helper(self, value):
        """Helper method to remove value and replace with in-order successor. (copied from my bst assignment.)"""
        # we're empty!
        if self.root is None:
            return False

        if value == self.root.value:
            return self.remove_first()

        def rec_contains(node):
            # value isn't in the tree
            if node is None:
                return False
            # left
            elif value < node.value:
                n_and_pn.push(node)
                if value == node.value:
                    return True
                else:
                    return rec_contains(node.left)
            # right
            elif value >= node.value:
                n_and_pn.push(node)
                if value == node.value:
                    return True
                else:
                    return rec_contains(node.right)

        n_and_pn = Stack()
        result = rec_contains(self.root)
        if result is False:
            return False

        node = n_and_pn.pop()
        parent_node = n_and_pn.pop()

        # N has no children
        if node.left is None and node.right is None:
            if parent_node.left is node:
                parent_node.left = None
                return parent_node
            else:
                parent_node.right = None
                return parent_node

        # N has one child
        elif node.left is None and node.right is not None or node.left is not None and node.right is None:
            # parent has open slot on right
            if parent_node.left is not None and parent_node.right is None and parent_node.left is not node:
                # N's child is on the left
                if node.left is not None and node.right is None:
                    parent_node.right = node.left
                    parent_node.right.parent = parent_node
                    return parent_node
                # N's child is on the right
                elif node.left is None and node.right is not None:
                    parent_node.right = node.right
                    parent_node.right.parent = parent_node
                    return parent_node
            # parent has an open slot on the left
            elif parent_node.left is None and parent_node.right is not None and parent_node.right is not node:
                # N's child is on the left
                if node.left is not None and node.right is None:
                    parent_node.left = node.left
                    parent_node.left.parent = parent_node
                    return parent_node
                # N's child is on the right
                elif node.left is None and node.right is not None:
                    parent_node.left = node.right
                    parent_node.left.parent = parent_node
                    return parent_node
            # parent has two children
            else:
                # N is PN's left child
                if parent_node.left is node:
                    # N's child is on the left
                    if node.left is not None and node.right is None:
                        parent_node.left = node.left
                        parent_node.left.parent = parent_node
                        return parent_node
                    # N's child is on the right
                    else:
                        parent_node.left = node.right
                        parent_node.left.parent = parent_node
                        return parent_node
                # N is PN's right child
                else:
                    # N's child is on the left
                    if node.left is not None and node.right is None:
                        parent_node.right = node.left
                        parent_node.right.parent = parent_node
                        return parent_node
                    # N's child is on the right
                    else:
                        parent_node.right = node.right
                        parent_node.right.parent = parent_node
                        return parent_node

        # the dreaded two child
        elif node.right is not None and node.left is not None:
            def rec_successor(node):
                if node.left is None:
                    s_and_ps.enqueue(node)
                    return s_and_ps
                s_and_ps.dequeue()
                s_and_ps.enqueue(node)
                return rec_successor(node.left)

            s_and_ps = Queue()
            s_and_ps.enqueue(node)  # start s_and_ps off with the node we're removing
            rec_successor(node.right)  # pass in node's right child to go down right tree

            # save S and PS
            parent_successor = s_and_ps.dequeue()
            successor = s_and_ps.dequeue()

            # print("successor is: " + str(successor))
            # print("successor parent is: " + str(parent_successor))

            successor.left = node.left
            successor.left.parent = successor

            if successor is not node.right:
                parent_successor.left = successor.right
                if parent_successor.left is not None:
                    parent_successor.left.parent = parent_successor
                successor.right = node.right
                successor.right.parent = successor
            # node was parent's left child
            if parent_node.left is node:
                parent_node.left = successor
                parent_node.left.parent = parent_node
                return parent_node
            # node was parent's right child
            else:
                parent_node.right = successor
                parent_node.right.parent = parent_node
                return parent_node

            # # parent node and successor are not adjacent
            # if successor is not node.right:
            #     parent_successor.left = successor.right
            #     successor.right = node.right
            #     # successor.parent = node.parent
            #
            #     return parent_node
            #
            # # parent node and successor are adjacent
            # elif successor.value < parent_node.value:
            #     parent_node.left = successor
            #     parent_node.left.parent = parent_node
            #     return parent_node
            # elif successor.value >= parent_node.value:
            #     parent_node.right = successor
            #     parent_node.right.parent = parent_node
            #     return parent_node

    def remove_first(self):
        """Removes the root node from the Binary Tree. Returns False if the tree is empty and True is the root is
        removed. (copied from my bst)"""

        # node = self.root

        # we're empty!
        if self.root is None:
            return False

        # it's just the root
        if self.root.left is None and self.root.right is None:
            self.root = None
            return None

        # root only has one child
        if self.root.left is None and self.root.right is not None or \
                self.root.left is not None and self.root.right is None:
            # child is on left
            if self.root.right is None:
                self.root = self.root.left
                return self.root
            # child is on right
            else:
                self.root = self.root.right
                return self.root

        # root has two children
        # find successor
        def rec_successor(node):
            if node.left is None:  # we've reached deepest left down the right tree
                s_and_ps.enqueue(node)
                return s_and_ps
            s_and_ps.dequeue()
            s_and_ps.enqueue(node)
            return rec_successor(node.left)

        # node = self.root

        s_and_ps = Queue()
        s_and_ps.enqueue(self.root)
        rec_successor(self.root.right)  # start moving down right tree

        # save S and PS
        parent_successor = s_and_ps.dequeue()
        successor = s_and_ps.dequeue()

        if self.root.left is successor:
            successor.right = self.root.right
            self.root = successor
            self.root.parent = None
            return self.root

        if self.root.right is successor:
            successor.left = self.root.left
            self.root = successor
            self.root.parent = None
            return self.root  # return the root to see if we need to do any rotations

        else:
            successor.left = self.root.left
            if successor is not self.root.right:
                parent_successor.left = successor.right
                if parent_successor.left is not None:
                    parent_successor.left.parent = parent_successor
                successor.right = self.root.right
                self.root.right.parent = successor
            self.root = successor
            self.root.parent = None
            return parent_successor  # return successor's parent to see if we need to do any rotations

    def update_height(self, node):
        # node has two children
        if node.left is not None and node.right is not None:
            node.height = max(node.left.height, node.right.height) + 1
        # node has no children
        elif node.left is None and node.right is None:
            node.height = 0
        # node has a left child
        elif node.left is not None and node.right is None:
            node.height = node.left.height + 1
        # node has a right child
        else:
            node.height = node.right.height + 1

    def balance_factor(self, node):
        """Returns the balance factor at specified node."""
        # return self.height(node.right) - self.height(node.left)

        # no children
        if node.left is None and node.right is None:
            return 0
        # two children
        elif node.left is not None and node.right is not None:
            return node.right.height - node.left.height
        # only a left child
        elif node.left is not None and node.right is None:
            return -1 - node.left.height
        # only a right child
        elif node.left is None and node.right is not None:
            return node.right.height + 1


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

    print("\nCustom - method remove() example A")
    print("-------------------------------")
    avl = AVL([1, 2, 3, 4, 5])
    avl.remove(7)
    print("Result: ", avl)


    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),                             # no AVL rotation
        ((1, 2, 3), 2),                             # no AVL rotation
        ((1, 2, 3), 3),                             # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),     # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),     # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),     # no AVL rotation
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)


    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),     # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),     # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),     # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),     # LR
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)


    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    avl = AVL(case)
    for del_value in case:
        print('INPUT  :', avl, del_value)
        avl.remove(del_value)
        print('RESULT :', avl)


    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    avl = AVL(case)
    for _ in case[:-2]:
        print('INPUT  :', avl.size(), avl, avl.root)
        avl.remove(avl.root.value)
        print('RESULT :', avl)


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


    """ Comprehensive example 1 """
    print("\nComprehensive example 1")
    print("-----------------------")
    tree = AVL()
    header = 'Value   Size  Height   Leaves   Unique   '
    header += 'Complete?  Full?    Perfect?'
    print(header)
    print('-' * len(header))
    print(f'  N/A {tree.size():6} {tree.height():7} ',
          f'{tree.count_leaves():7} {tree.count_unique():8}  ',
          f'{str(tree.is_complete()):10}',
          f'{str(tree.is_full()):7} ',
          f'{str(tree.is_perfect())}')

    for value in [10, 5, 3, 15, 12, 8, 20, 1, 4, 9, 7]:
        tree.add(value)
        print(f'{value:5} {tree.size():6} {tree.height():7} ',
              f'{tree.count_leaves():7} {tree.count_unique():8}  ',
              f'{str(tree.is_complete()):10}',
              f'{str(tree.is_full()):7} ',
              f'{str(tree.is_perfect())}')
    print()
    print(tree.pre_order_traversal())
    print(tree.in_order_traversal())
    print(tree.post_order_traversal())
    print(tree.by_level_traversal())


    """ Comprehensive example 2 """
    print("\nComprehensive example 2")
    print("-----------------------")
    tree = AVL()
    header = 'Value   Size  Height   Leaves   Unique   '
    header += 'Complete?  Full?    Perfect?'
    print(header)
    print('-' * len(header))
    print(f'N/A   {tree.size():6} {tree.height():7} ',
          f'{tree.count_leaves():7} {tree.count_unique():8}  ',
          f'{str(tree.is_complete()):10}',
          f'{str(tree.is_full()):7} ',
          f'{str(tree.is_perfect())}')

    for value in 'DATA STRUCTURES':
        tree.add(value)
        print(f'{value:5} {tree.size():6} {tree.height():7} ',
              f'{tree.count_leaves():7} {tree.count_unique():8}  ',
              f'{str(tree.is_complete()):10}',
              f'{str(tree.is_full()):7} ',
              f'{str(tree.is_perfect())}')
    print('', tree.pre_order_traversal(), tree.in_order_traversal(),
          tree.post_order_traversal(), tree.by_level_traversal(),
          sep='\n')
