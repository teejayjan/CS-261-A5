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

        return self.heap[0]

    def remove_min(self) -> object:
        """Returns an object with a minimum key and removes it from the heap. Raises an exception if the heap is
        empty."""

        if self.is_empty():
            raise MinHeapException

        min = self.get_min()
        self.heap.swap(0, self.heap.length() - 1)
        self.heap.pop()

        def rec_min(i, l, r):
            """Recursive remove_min helper."""
            if l > self.heap.length() - 1 and r > self.heap.length() - 1:
                return
            # just left is in bounds
            if l <= self.heap.length() <= r:
                if self.heap[i] > self.heap[l]:
                    self.heap.swap(i, l)
                return
            # left is minimum
            elif self.heap[l] < self.heap[r] and self.heap[i] > self.heap[l]:
                self.heap.swap(i, l)
                return rec_min(l, (l * 2) + 1, (l * 2) + 2)
            # right is minimum
            elif self.heap[r] < self.heap[l] and self.heap[i] > self.heap[r]:
                self.heap.swap(i, r)
                return rec_min(r, (r * 2) + 1, (r * 2) + 2)

        rec_min(0, 1, 2)
        return min

    def build_heap(self, da: DynamicArray) -> None:
        """Receives a Dynamic Array and builds a proper MinHeap. Current contents of MinHeap are lost upon calling
        this method."""

        self.heap = DynamicArray()
        for i in range(da.length()):
            self.heap.append(da[i])

        def rec_build(nli, i, l, r):
            """Recursive build_heap helper."""
            if nli < 0:
                return
            # we're at the end with that non-leaf-index
            if l > self.heap.length() and r > self.heap.lengt():
                return rec_build(nli - 1, nli - 1, ((nli - 1) * 2 + 1), ((nli - 1) * 2 + 2))
            # left
            elif self.heap[l] < self.heap[r] and self.heap[i] > self.heap[l]:
                self.heap.swap(i, l)
                return rec_build(nli, l, (l * 2) + 1, (l * 2) + 2)
            # right
            elif self.heap[l] > self.heap[r] and self.heap[i] > self.heap[r]:
                self.heap.swap(i, r)
                return rec_build(nli, r, (r * 2) + 1, (r * 2) + 2)
            return rec_build(nli - 1, nli - 1, ((nli - 1) * 2 + 1), ((nli - 1) * 2 + 2))

        non_leaf_index = (da.length() // 2) - 1
        rec_build(non_leaf_index, non_leaf_index, non_leaf_index * 2 + 1, non_leaf_index * 2 + 2)


# BASIC TESTING
if __name__ == '__main__':

    # print("\nPDF - add example 1")
    # print("-------------------")
    # h = MinHeap()
    # print(h, h.is_empty())
    # for value in range(300, 200, -15):
    #     h.add(value)
    #     print(h)
    #
    # print("\nPDF - add example 2")
    # print("-------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
    #     h.add(value)
    #     print(h)
    #
    # print("\nPDF - get_min example 1")
    # print("-----------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # print(h.get_min(), h.get_min())
    #
    # print("\nPDF - remove_min example 1")
    # print("--------------------------")
    # h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    # while not h.is_empty():
    #     print(h, end=' ')
    #     print(h.remove_min())
    #
    # print("\nCustom - remove-min example A")
    # print("-----------------------------")
    # h = MinHeap([-657, -649, -626, -612, -644, -622, -614, -582, -609, -601, -643, -578, -622, -560, -563, -562, -540, -606, -584, -568, -573, -634, -617, -436, -553, -561, -535, -296, -397, -331, -411, -357, -230, -520, -405, -596, -540, -490, -523, -459, -402, -536, -347, -623, -519, -569, -354, -292, -394, -524, -519, -424, -386, -182, -364, 136, -112, -57, -228, -66, 48, -305, -351, -352, -272, -107, -69, -230, -334, -117, -354, -265, -212, -515, -533, -115, -300, -369, -353, -415, -63, -258, 145, -178, -390, -59, -313, -215, -462, -390, -490, 162, -508, -244, 29, 25, 172, -310, -232, -361, -133, -469, -361, -79, -312, -124, -121, 127, 32, 43, 311, 152, 338, -102, 541, 150, -54, 142, -170, 147, 441, 298, 69, 440, 17, 390, 444, 577, -166, 56, 402, 86, 335, 544, 299, 20, 147, 358, 203, 841, 56, -322, -330, -176, 227, -78, 670, -478, -375, -119, -248, 487, 274, -287, 257, -286, -345, -295, 55, 50, 46, 83, 95, 242, 147, 208, 638, 166, 153, 6, -385, 453, 47, -219, -64, -25, 401, -57, 363, 89, 353, -427, 286, 227, 246, -379, 309, -212, 400, 153, 496, 626, 28, 363, 456, 562, -289, 509, 426, 102, 440, 154, 44, -122, 724, -131, 436, 590, 577, -255, -71, -72, 570, 169, 578, 888, 784, 241, 40, 439, 428, 752, 633, 847, 843, 358, 951, 410, 58, 748, 907, 657, 571, 165, 163, 244, 424, 217, 868, 486, 453, 689, 782, 421, 303, 889, 241, 623, 762, 169, 642, 816, 628, 932, 770, 913, 764, 922, 477, 708, 303, 696, 818, 576, 212, 519, 569, 550, 588, 870, 608, 216, 538, 996, 676, 877, 997, 613, 511, 955, 919, 677, 725, 837, 226, 910, 808, 346, 300, 782, 695, -60, 970, 897, 777, 792, -38, 543, 123, 402, 258, -40, -57, 513, 939, 592, 643, 559, 453, 444, 459, 760, 136, 334, 87, 622, 486, 698, 637, 536, 359, 505, 551, 313, 352, 948, 135, 891, 552, 613, 406, 408, 439, 777, 727, 734, 511, 282, 425, 293, 177, -175, 938, 978, 899, 539, 490, 825, 38, 955, 383, 908, 684, 751, 586, 626, 776])
    # h.remove_min()
    # print(h)

    #
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
