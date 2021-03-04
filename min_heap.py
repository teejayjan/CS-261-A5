# Course: CS261 - Data Structures
# Assignment: 5
# Student: Timothy Jan
# Description: Implements min heap.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """Adds a new object to the MinHeap maintaining heap property."""

        self.heap.append(node)
        node_index = self.heap.length() - 1
        parent_index = (self.heap.length() - 2) // 2  # initial parent index length - 2 to account for zero index

        if node_index <= 0:
            return

        while self.heap.get_at_index(node_index) < self.heap.get_at_index(parent_index):
            self.heap.swap(node_index, parent_index)
            node_index = parent_index
            parent_index = (node_index - 1) // 2
            if node_index <= 0:
                break

    def get_min(self) -> object:
        """Returns an object with a minimum key without removing it from the heap. Raises an exception if
        the heap is empty."""

        if self.is_empty():
            raise MinHeapException

        return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """Returns an object with a minimum key and removes it from the heap. Raises an exception if the heap is
        empty."""

        if self.is_empty():
            raise MinHeapException

        # save min
        min = self.get_min()

        # array is larger than 1 element
        if self.heap.length() > 3:
            # swap first and last, remove last
            self.heap.swap(0, self.heap.length() - 1)
            self.heap.pop()
            # assign starting indices
            node_index = 0
            left_child_index = 1
            right_child_index = 2
            # iterate until both children are out of bounds
            while left_child_index < self.heap.length() and right_child_index < self.heap.length():
                # if only left child is in bounds
                if left_child_index < self.heap.length() < right_child_index:
                    if self.heap.get_at_index(node_index) > self.heap.get_at_index(left_child_index):
                        self.heap.swap(node_index, left_child_index)
                # check left
                elif left_child_index < self.heap.length() and self.heap.get_at_index(left_child_index) <= \
                        self.heap.get_at_index(right_child_index):
                    if self.heap.get_at_index(node_index) > self.heap.get_at_index(left_child_index):
                        self.heap.swap(node_index, left_child_index)
                    node_index = left_child_index
                    left_child_index = (node_index * 2) + 1
                    right_child_index = (node_index * 2) + 2
                # check right
                elif right_child_index < self.heap.length() and self.heap.get_at_index(left_child_index) > \
                        self.heap.get_at_index(right_child_index):
                    if self.heap.get_at_index(node_index) > self.heap.get_at_index(right_child_index):
                        self.heap.swap(node_index, right_child_index)
                    node_index = right_child_index
                    left_child_index = (node_index * 2) + 1
                    right_child_index = (node_index * 2) + 2
            return min

        # special cases for specific heap sizes
        elif self.heap.length() == 3:
            self.heap.swap(0, 2)
            self.heap.pop()
            if self.heap.get_at_index(0) > self.heap.get_at_index(1):
                self.heap.swap(0, 1)
            return min

        elif self.heap.length() == 2:
            self.heap.swap(0, 1)
            self.heap.pop()
            return min

        else:
            self.heap.pop()
            return min

    def build_heap(self, da: DynamicArray) -> None:
        """Receives a Dynamic Array and builds a proper MinHeap. Current contents of MinHeap are lost upon calling
        this method."""

        self.heap = DynamicArray()
        for i in range(da.length()):
            self.heap.append(da.get_at_index(i))
        non_leaf_index = (da.length() // 2) - 1

        # examine non-leaf nodes until we've checked through the root
        while non_leaf_index >= 0:
            # save indices
            node_index = non_leaf_index
            left_child_index = (node_index * 2) + 1
            right_child_index = (node_index * 2) + 2

            # percolate non-leaf node downward
            while left_child_index < self.heap.length() and right_child_index < self.heap.length():
                # only a left child
                if left_child_index < self.heap.length() < right_child_index:
                    if self.heap.get_at_index(node_index) > self.heap.get_at_index(left_child_index):
                        self.heap.swap(node_index, left_child_index)
                # check left
                elif left_child_index < self.heap.length() and self.heap.get_at_index(left_child_index) <= \
                        self.heap.get_at_index(right_child_index):
                    if self.heap.get_at_index(node_index) > self.heap.get_at_index(left_child_index):
                        self.heap.swap(node_index, left_child_index)
                    node_index = left_child_index
                    left_child_index = (node_index * 2) + 1
                    right_child_index = (node_index * 2) + 2
                # check right
                elif right_child_index < self.heap.length() and self.heap.get_at_index(left_child_index) > \
                        self.heap.get_at_index(right_child_index):
                    if self.heap.get_at_index(node_index) > self.heap.get_at_index(right_child_index):
                        self.heap.swap(node_index, right_child_index)
                    node_index = right_child_index
                    left_child_index = (node_index * 2) + 1
                    right_child_index = (node_index * 2) + 2
            non_leaf_index -= 1


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
