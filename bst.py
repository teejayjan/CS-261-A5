# Course: CS261 - Data Structures
# Student Name: Timothy Jan
# Assignment: Assignment 4 - Your Very Own BST Tree
# Description: Implements a binary search tree.


class Stack:
    """
    Class implementing STACK ADT.
    Supported methods are: push, pop, top, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty stack based on Python list """
        self._data = []

    def push(self, value: object) -> None:
        """ Add new element on top of the stack """
        self._data.append(value)

    def pop(self) -> object:
        """ Remove element from top of the stack and return its value """
        return self._data.pop()

    def top(self) -> object:
        """ Return value of top element without removing from stack """
        return self._data[-1]

    def is_empty(self):
        """ Return True if the stack is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "STACK: { " + ", ".join(data_str) + " }"


class Queue:
    """
    Class implementing QUEUE ADT.
    Supported methods are: enqueue, dequeue, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty queue based on Python list """
        self._data = []

    def enqueue(self, value: object) -> None:
        """ Add new element to the end of the queue """
        self._data.append(value)

    def dequeue(self) -> object:
        """ Remove element from the beginning of the queue and return its value """
        return self._data.pop(0)

    def is_empty(self):
        """ Return True if the queue is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "QUEUE { " + ", ".join(data_str) + " }"


class TreeNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Init new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None  # pointer to root of left subtree
        self.right = None  # pointer to root of right subtree

    def __str__(self):
        return str(self.value)


class BST:
    def __init__(self, start_tree=None) -> None:
        """
        Init new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of BST in human-readable form using in-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self.root, values)
        return "TREE pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, cur, values):
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # base case
        if not cur:
            return
        # store value of current node
        values.append(str(cur.value))
        # recursive case for left subtree
        self._str_helper(cur.left, values)
        # recursive case for right subtree
        self._str_helper(cur.right, values)

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """Adds a new value to the tree."""

        def rec_add(node):
            # create root node if first added value
            if node is None:
                self.root = TreeNode(value)
            # go left!
            elif value < node.value:
                if node.left is not None:
                    return rec_add(node.left)
                elif node.left is None and value < node.value:
                    node.left = TreeNode(value)
            # go right!
            elif value >= node.value:
                if node.right is not None:
                    return rec_add(node.right)
                elif node.right is None and value >= node.value:
                    node.right = TreeNode(value)

        rec_add(self.root)

    def contains(self, value: object) -> bool:
        """Returns True if the value is found in the Binary Tree, otherwise, returns False. """

        def rec_contains(node):
            # we're empty!
            if self.root is None:
                return False
            # we're at the end of the road and didn't find your value
            elif node is None:
                return False
            # go left!
            elif value < node.value:
                if value == node.value:  # is this your value?
                    return True
                return rec_contains(node.left)  # otherwise, keep going
            # go right!
            elif value >= node.value:
                if value == node.value:
                    return True
                return rec_contains(node.right)

        return rec_contains(self.root)

    def get_first(self) -> object:
        """Returns the value stored at the root node."""

        # we're empty!
        if self.root is None:
            return None
        return self.root.value

    def remove(self, value) -> bool:
        """Removes the first instance of the value in the BinaryTree. Returns True if the value is removed, otherwise
        returns False."""

        # we're empty!
        if self.root is None:
            return False

        if value == self.root.value:
            self.remove_first()
            return True

        # find N/PN
        def rec_contains(node):
            # we didn't find the value
            if node is None:
                while not n_and_pn.is_empty():
                    n_and_pn.pop()
                return False
            # go left!
            elif value < node.value:
                n_and_pn.push(node)
                if value == node.value:
                    return n_and_pn
                return rec_contains(node.left)
            # go right!
            elif value >= node.value:
                n_and_pn.push(node)
                if value == node.value:
                    return n_and_pn
                return rec_contains(node.right)

        n_and_pn = Stack()
        rec_contains(self.root)

        if n_and_pn.is_empty():
            return False

        node = n_and_pn.pop()
        parent_node = n_and_pn.pop()

        # print(parent_node)
        # print(node)

        # N has no children
        if node.left is None and node.right is None:
            if parent_node.left is node:
                parent_node.left = None
                return True
            else:
                parent_node.right = None
                return True

        # N has one child
        elif node.left is None and node.right is not None or node.left is not None and node.right is None:
            # parent has open slot on right
            if parent_node.left is not None and parent_node.right is None and parent_node.left is not node:
                # N's child is on the left
                if node.left is not None and node.right is None:
                    parent_node.right = node.left
                    return True
                # N's child is on the right
                elif node.left is None and node.right is not None:
                    parent_node.right = node.right
                    return True
            # parent has an open slot on the left
            elif parent_node.left is None and parent_node.right is not None and parent_node.right is not node:
                # N's child is on the left
                if node.left is not None and node.right is None:
                    parent_node.right = node.left
                    return True
                # N's child is on the right
                elif node.left is None and node.right is not None:
                    parent_node.right = node.right
                    return True
            # parent has two children
            else:
                # N is PN's left child
                if parent_node.left is node:
                    # N's child is on the left
                    if node.left is not None and node.right is None:
                        parent_node.left = node.left
                        return True
                    # N's child is on the right
                    else:
                        parent_node.left = node.right
                        return True
                # N is PN's right child
                else:
                    # N's child is on the left
                    if node.left is not None and node.right is None:
                        parent_node.right = node.left
                        return True
                    # N's child is on the right
                    else:
                        parent_node.right = node.right
                        return True

        # the dreaded two child
        elif node.right and node.left:
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

            if successor != node.right:
                parent_successor.left = successor.right
                successor.right = node.right

            # update parent node to point to successor instead of node
            if successor.value < parent_node.value:
                parent_node.left = successor
                return True
            elif successor.value >= parent_node.value:
                parent_node.right = successor
                return True

    def remove_first(self) -> bool:
        """Removes the root node from the Binary Tree. Returns False if the tree is empty and True is the root is
        removed."""

        node = self.root

        # we're empty!
        if self.root is None:
            return False

        # it's just the root
        if self.root.left is None and self.root.right is None:
            self.root = None
            return True

        # root only has one child
        if self.root.left is None and self.root.right is not None or \
                self.root.left is not None and self.root.right is None:
            # child is on left
            if node.right is None:
                self.root = node.left
                return True
            # child is on right
            else:
                self.root = node.right
                return True

        # root has two children

        # find successor
        def rec_successor(node):
            if node.left is None:  # we've reached deepest left down the right tree
                s_and_ps.enqueue(node)
                return s_and_ps
            s_and_ps.dequeue()
            s_and_ps.enqueue(node)
            return rec_successor(node.left)

        s_and_ps = Queue()
        s_and_ps.enqueue(node)
        rec_successor(node.right)  # start moving down right tree

        # save S and PS
        parent_successor = s_and_ps.dequeue()
        successor = s_and_ps.dequeue()

        if node.left is successor:
            successor.right = node.right
            self.root = successor
            return True

        if node.right is successor:
            successor.left = node.left
            self.root = successor
            return True

        else:
            successor.left = node.left
            if successor is not node.right:
                parent_successor.left = successor.right
                successor.right = node.right
            self.root = successor
            return True

    def pre_order_traversal(self) -> Queue:
        """Returns a Queue containing values of visited nodes in pre-order traversal order."""

        return_queue = Queue()

        # we're empty
        if self.size == 0:
            return return_queue

        def rec_pre_order(node):
            if node is None:
                return return_queue
            return_queue.enqueue(node.value)
            rec_pre_order(node.left)
            rec_pre_order(node.right)

        rec_pre_order(self.root)
        return return_queue

    def in_order_traversal(self) -> Queue:
        """Returns a Queue containing values of visited nodes in in-order traversal order."""

        return_queue = Queue()

        # we're empty
        if self.size == 0:
            return return_queue

        def rec_in_order(node):
            if node is None:
                return return_queue
            rec_in_order(node.left)
            return_queue.enqueue(node.value)
            rec_in_order(node.right)

        rec_in_order(self.root)
        return return_queue

    def post_order_traversal(self) -> Queue:
        """Returns a Queue containing values of visited nodes in post-order traversal order."""

        return_queue = Queue()

        # we're empty
        if self.size == 0:
            return return_queue

        def rec_post_order(node):
            if node is None:
                return return_queue
            rec_post_order(node.left)
            rec_post_order(node.right)
            return_queue.enqueue(node.value)

        rec_post_order(self.root)
        return return_queue

    def by_level_traversal(self) -> Queue:
        """Returns a Queue containing values of visited nodes in by-level traversal order."""

        return_queue = Queue()
        temp_queue = Queue()

        # we're empty!
        if self.size == 0:
            return return_queue

        temp_queue.enqueue(self.root)
        while not temp_queue.is_empty():
            node = temp_queue.dequeue()
            if node is not None:
                return_queue.enqueue(node)
                temp_queue.enqueue(node.left)
                temp_queue.enqueue(node.right)

        return return_queue

    def size(self) -> int:
        """Returns the total number of nodes in the tree."""

        count = 0
        temp_queue = Queue()

        # we're empty!
        if self.size == 0:
            return 0

        temp_queue.enqueue(self.root)
        while not temp_queue.is_empty():
            node = temp_queue.dequeue()
            if node is not None:
                count += 1
                temp_queue.enqueue(node.left)
                temp_queue.enqueue(node.right)

        return count

    def height(self) -> int:
        """Returns the height of the binary tree. Empty tree returns -1, and a single root node returns 0."""

        # we're empty!
        if self.size() == 0:
            return -1

        # nothing but the root
        elif self.root.left is None and self.root.right is None:
            return 0

        # otherwise...
        else:
            def rec_height(node):
                left_height = 0
                right_height = 0
                # traverses left and right trees, returning 1 each time we hit a dead end, until the final dead end
                # which is the height of the tree; saves each height pass to the left/right height variables
                if node.left is not None:
                    left_height = rec_height(node.left)
                if node.right is not None:
                    right_height = rec_height(node.right)
                if left_height > right_height:
                    return left_height + 1
                else:
                    return right_height + 1

            # return height - 1 since we passed in root (technically starting at height of 1)
            return rec_height(self.root) - 1

    def count_leaves(self) -> int:
        """Returns the number of nodes in the tree that have no children. If the tree is empty, returns 0."""

        # we're empty!
        if self.size() == 0:
            return 0

        count = 0
        temp_queue = Queue()

        # modified by-level traversal that adds 1 to count every time we encounter a node with no children (leaf)
        temp_queue.enqueue(self.root)
        while not temp_queue.is_empty():
            node = temp_queue.dequeue()
            if node is not None:
                if node.left is None and node.right is None:
                    count += 1
                temp_queue.enqueue(node.left)
                temp_queue.enqueue(node.right)

        return count

    def count_unique(self) -> int:
        """Returns a count of the unique values stored in the tree. If all values are distinct, method returns
        same result as size() method."""

        # we're empty!
        if self.size() == 0:
            return 0

        # get ourselves a queue of the tree in order
        comparison_queue = self.in_order_traversal()

        count = 0
        # get us a stack
        temp_stack = Stack()

        # add the first value from the queue to the stack
        temp_stack.push(comparison_queue.dequeue())
        # add one to count since we're not really comparing it against anything yet
        count += 1

        # compare the next value in the queue to the top of the stack
        while not comparison_queue.is_empty():
            current = comparison_queue.dequeue()
            if current != temp_stack.top():
                # if current is not equal to the top of the stack, we add 1 to count to reflect unique values
                count += 1
            temp_stack.push(current)

        return count

    def is_complete(self) -> bool:
        """Returns True if the current tree is a 'complete binary tree'. Empty trees and trees with one root node
        are considered complete."""

        # empty or one root node
        if self.size() == 0 or self.root.left is None and self.root.right is None:
            return True

        # root has only one child but more than two nodes
        if self.root.left is None and self.root is not None and self.size() > 2 or \
                self.root.right is None and self.root.left is not None and self.size() > 2:
            return False

        else:
            # create a by-level traversal to iterate through
            temp_queue = self.by_level_traversal()

            # tracks when we encounter our first leaf (which if complete should be the last node encountered)
            first_leaf_flag = False

            # modified by-level traversal, where we return False if we encounter more than one node with only a
            # left child, or encounter a node with two children after already encountering a leaf (many leaves in a
            # row are OK)
            while not temp_queue.is_empty():
                node = temp_queue.dequeue()
                # node with only one right child can never be complete
                if node.left is None and node.right is not None:
                    return False

                # a node with two children comes after a leaf node
                if node.left is not None and node.right is not None and first_leaf_flag:
                    return False

                # a node with only one left child comes after a leaf, or another node with only one left child
                if node.left is not None and node.right is None and first_leaf_flag:
                    return False

                # DISQUALIFYING CASES
                # encounter our first leaf
                if node.left is None and node.right is None:
                    first_leaf_flag = True
                # encounter our first node with only one left child
                if node.left is not None and node.right is None:
                    first_leaf_flag = True

            return True

    def is_full(self) -> bool:
        """Returns True if the current tree is a 'full binary tree'. Empty trees and trees with one root node
        are considered 'full'."""

        # empty or one root node
        if self.size() == 0 or self.root.left is None and self.root.right is None:
            return True

        else:
            temp_queue = Queue()

            temp_queue.enqueue(self.root)
            while not temp_queue.is_empty():
                node = temp_queue.dequeue()
                if node is not None:
                    # as we iterate, if we ever encounter a node with 1 child, return False
                    if node.left is None and node.right is not None:
                        return False
                    elif node.right is None and node.left is not None:
                        return False
                    temp_queue.enqueue(node.left)
                    temp_queue.enqueue(node.right)
            return True

    def is_perfect(self) -> bool:
        """Returns True if the current tree is a 'perfect binary tree'. Empty trees and trees with one root node
        are considered 'perfect'."""

        # empty or one root node
        if self.size() == 0 or self.root.left is None and self.root.right is None:
            return True

        # perfect trees must also be full
        elif not self.is_full():
            return False

        else:
            height = self.height()
            leaves = self.count_leaves()
            # doesn't have 2**h leaves
            if leaves != 2 ** height:
                return False
            # doesn't have (2**h+1)-1 total nodes
            nodes = self.size()
            if nodes != (2 ** (height + 1)) - 1:
                return False
            return True


# BASIC TESTING - PDF EXAMPLES

if __name__ == '__main__':
    # """ add() example #1 """
    # print("\nPDF - method add() example 1")
    # print("----------------------------")
    # tree = BST()
    # print(tree)
    # tree.add(10)
    # tree.add(15)
    # tree.add(5)
    # print(tree)
    # tree.add(15)
    # tree.add(15)
    # print(tree)
    # tree.add(5)
    # print(tree)
    #
    # """ add() example 2 """
    # print("\nPDF - method add() example 2")
    # print("----------------------------")
    # tree = BST()
    # tree.add(10)
    # tree.add(10)
    # print(tree)
    # tree.add(-1)
    # print(tree)
    # tree.add(5)
    # print(tree)
    # tree.add(-1)
    # print(tree)

    # """ contains() example 1 """
    # print("\nPDF - method contains() example 1")
    # print("---------------------------------")
    # tree = BST([10, 5, 15])
    # print(tree.contains(15))
    # print(tree.contains(-10))
    # print(tree.contains(15))
    #
    # """ contains() example 2 """
    # print("\nPDF - method contains() example 2")
    # print("---------------------------------")
    # tree = BST()
    # print(tree.contains(0))
    #
    # """ get_first() example 1 """
    # print("\nPDF - method get_first() example 1")
    # print("----------------------------------")
    # tree = BST()
    # print(tree.get_first())
    # tree.add(10)
    # tree.add(15)
    # tree.add(5)
    # print(tree.get_first())
    # print(tree)
    #
    """ remove() example 1 """
    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    tree = BST([10, 5, 15])
    print(tree.remove(7))
    print(tree.remove(15))
    print(tree.remove(15))

    """ remove() example 2 """
    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.remove(20))
    print(tree)

    """ remove() example 3 """
    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    tree = BST([10, 5, 20, 18, 12, 7, 27, 22, 18, 24, 22, 30])
    print(tree.remove(20))
    print(tree)
    # comment out the following lines
    # if you have not yet implemented traversal methods
    print(tree.pre_order_traversal())
    print(tree.in_order_traversal())
    print(tree.post_order_traversal())
    print(tree.by_level_traversal())
    #
    """ remove_first() example 1 """
    print("\nPDF - method remove_first() example 1")
    print("-------------------------------------")
    tree = BST([10, 15, 5])
    print(tree.remove_first())
    print(tree)

    """ remove_first() example 2 """
    print("\nPDF - method remove_first() example 2")
    print("-------------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7])
    print(tree.remove_first())
    print(tree)

    """ remove_first() example 3 """
    print("\nPDF - method remove_first() example 3")
    print("-------------------------------------")
    tree = BST([10, 10, -1, 5, -1])
    print(tree.remove_first(), tree)
    print(tree.remove_first(), tree)
    print(tree.remove_first(), tree)
    print(tree.remove_first(), tree)
    print(tree.remove_first(), tree)
    print(tree.remove_first(), tree)
    #
    # """ Traversal methods example 1 """
    # print("\nPDF - traversal methods example 1")
    # print("---------------------------------")
    # tree = BST([10, 20, 5, 15, 17, 7, 12])
    # print(tree.pre_order_traversal())
    # print(tree.in_order_traversal())
    # print(tree.post_order_traversal())
    # print(tree.by_level_traversal())
    #
    # """ Traversal methods example 2 """
    # print("\nPDF - traversal methods example 2")
    # print("---------------------------------")
    # tree = BST([10, 10, -1, 5, -1])
    # print(tree.pre_order_traversal())
    # print(tree.in_order_traversal())
    # print(tree.post_order_traversal())
    # print(tree.by_level_traversal())
    #
    # """ Comprehensive example 1 """
    # print("\nComprehensive example 1")
    # print("-----------------------")
    # tree = BST()
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
    # tree = BST()
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
    #
    # print("test case 1")
    # tree = BST(["L", "JP", "C", "PB", "NO", "XX"])
    # print(tree.by_level_traversal())
    # print(tree.is_complete())
    #
    # print("test case 2")
    # tree = BST([-7680, -8377, -123, -7113, -118])
    # print(tree.by_level_traversal())
    # print(tree.is_complete())

    print("remove test 1")
    tree = BST([0, 1, 2, 2, 3, 3, 3])
    tree.remove(0)
    print(tree)

    print("remove test 2")
    tree = BST([15, 5, 7, 20, 17])
    tree.remove_first()
    print(tree)

    print("remove test 3")
    tree = BST([1, 2, 2, 3, 3, 3])
    tree.remove(2)
    print(tree)

    print("remove test 4")
    tree = BST([1, 2, 3, 3, 3])
    tree.remove(3)
    print(tree)

    print("remove test 5")
    tree = BST([10, 9, 6, 0, -6, 2, 6, 10])
    tree.remove(9)
    print(tree)

    # print("remove test 6")
    # tree = BST([2213, -73349, -87187, -87187, -87187, -87187, -46489, -64005, -37673, -41236, -46489, -46489, -37673,
    #            -37673,
    #            70382, 2978, 2329, 2213, 55070, 52833, 38001, 22582, 18697, 18697, 38001, 52833, 52833, 86437, 70382,
    #            70382, 86437]
    #            )
    # print(tree.remove(18697))
    # print(tree)

    print("remove test 7")
    tree = BST([-4, -9, -9, -8, -4, 9, 6, -1])
    tree.remove(-8)
    print(tree)

    print("remove test 8")
    tree = BST([40, 16, 50, 10, 19, 45, 92, 1, 15, 17, 35, 47, 75, 101])
    tree.remove(40)
    print(tree)
    tree.remove(50)
    print(tree)

