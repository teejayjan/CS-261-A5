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
            elif self.heap[l] <= self.heap[r] and self.heap[i] > self.heap[l]:
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
            # no need to swap, check next non leaf node
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

    print("\nCustom - remove-min example B")
    print("-----------------------------")
    h = MinHeap([-983, -982, -982, -971, -981, -977, -974, -963, -961, -968, -962, -920, -861, -956, -972, -922, -923, -904, -956, -954, -954, -945, -856, -848, -845, -674, -845, -879, -915, -944, -808, -613, -865, -766, -882, -719, -882, -872, -931, -913, -851, -879, -946, -910, -793, -836, -782, -837, -675, -788, -655, -322, -562, -688, -796, -869, -598, -572, -864, -664, -903, -807, -609, -330, -434, -806, -835, -389, -419, -752, -876, -535, -412, -829, -833, -667, -791, -844, -716, -886, -746, -785, -822, -178, -764, -858, -894, -832, -859, -414, -651, -775, -752, -770, -562, -810, -415, -512, -613, -227, -249, -456, -351, -272, -295, -376, -171, -511, -617, -785, -728, -836, -54, -502, -591, -234, -199, -434, -782, -590, -660, -803, -720, -312, -630, 263, -148, -270, -95, -148, -250, -656, -702, -779, -810, -352, -335, -337, -398, -246, -136, -660, -834, -367, -431, -363, -385, -705, -795, -804, -680, -144, -647, -119, -589, -842, -743, -401, -526, -755, -857, -573, -648, -775, -462, -306, -771, -2, -81, -677, -415, -372, -848, -558, -774, -660, -709, -798, -848, -396, -357, -536, -314, -486, -596, -724, -421, -565, -761, -192, -513, -373, -727, -415, -311, -170, -157, 275, -495, 424, 436, -186, 320, 764, -366, 485, 339, 671, -149, -215, -194, -75, -305, 241, 59, 123, -336, -133, -583, -621, -204, -486, -431, 131, 91, 155, 295, 151, -461, 251, -64, -69, -121, -138, 175, 409, 100, 0, -458, -489, -373, 70, -612, -690, 112, -351, -284, -65, -284, -590, -26, 612, 361, 680, -135, 682, -138, 290, 90, 220, 52, 86, -169, 5, -284, -542, -204, -279, -336, -481, -698, -101, 433, 438, -251, 209, -284, 513, 260, 5, -194, 133, -134, -378, 188, -552, -481, 124, -119, -286, 104, 311, -144, -104, -347, -416, -530, -698, 151, -771, -348, -138, -407, 734, 102, 315, -372, 252, 53, -175, 675, -575, -53, -618, -648, -133, -399, 33, -410, -670, -708, 167, -690, -377, 287, -644, -147, -761, -32, 41, 59, 510, -291, -197, -582, 674, 728, -46, 435, 192, -274, -150, -203, -359, -354, 18, -465, -224, -124, 257, -753, -13, -603, -431, -482, -268, -501, -27, -781, 296, -175, -2, -167, 222, -376, 262, -291, 418, -134, -356, -502, -96, -631, 70, -205, -454, 103, -401, -720, 441, -167, 299, -491, -288, 488, -617, -566, 214, 3, -210, -184, 195, 779, 708, 516, 852, 633, -103, -352, 914, 752, 864, 565, 767, 267, 911, 722, 878, 788, 853, -103, 781, 685, 960, 725, 884, 883, 612, 93, 627, 271, 776, 243, 721, 169, 632, -269, 807, 404, 560, 697, 941, 851, 337, 682, 507, 890, 59, 945, 614, 31, 139, 144, 379, 228, 857, 553, 946, 293, 725, 104, 729, 451, 994, 645, 640, 694, 651, 439, 718, 489, 793, 229, 445, 157, 198, 231, 167, 997, 873, 218, 876, 613, 427, 313, 341, 592, 76, -423, 502, 215, 20, 656, 586, 561, 79, -497, 441, -108, 420, 540, 860, 601, 846, 964, 768, 60, 0, -59, 666, -125, 987, 562, 973, 744, 866, 543, 991, 740, 783, 926, 847, 707, 694, -94, 321, 640, 178, 737, 811, 388, 257, 216, 90, 513, 474, -124, 646, 714, 999, 4, -97, -330, 494, -103, 700, 19, 842, 248, 720, 389, 549, -275, 638, 112, 948, 637, 968, 495, 243, 521, 926, 916, 468, 456, 974, 953, 450, 271, 768, 336, 555, 341, 681, 568, 263, -48, 739, 344, 770, 557, 206, -115, 204, -124, 882, 305, 193, 96, 335, 146, 732, 507, 809, 641, 434, 39, 689, 555, 526, 700, -7, -9, -46, 802, -386, -381, 620, 590, 490, -680, 616, -56, 541, 421, 814, -310, 798, 985, 294, 798, 372, 812, -92, -123, 716, 399, 444, 331, 685, -1, 973, 953, 839, -436, 905, -18, -80, 509, -90, -586, 878, 82, 73, -103, 645, 946, 394, 827, 612, -134, -8, -431, 798, 495, 445, 143, 461, 349, 575, 682, 153, 240, 505, 122, 695, 51, 116, -24, 188, 324, 305, 146, 549, 643, 937, -56, 429, -34, 921, 130, 935, 926, 772, 930, 888, 470, 821, 798, 819, 597, 955, 84, 789, 924, 169, 94, 397, 300, 730, -43, 682, 561, 681, -422, 839, -100, 358, 780, 969, 891, 237, -337, 591, 919, -76, -90, 914, -152, -61, 935, 617, 323, 681, 92, 944, 902, 485, 195, 932, 552, 634, 230, 981, 327, 263, -115, 608, 344, 519, 404, 514, 582, 880, 335, 984, 874, 155, 430, 434, 256, 235, -159, 911, -28, 878, 403, 953, 70, 504, 201, 330, -109, 880, 282, 544, 208, 579, 381, 665, 696, 50, 566, 698, 650, -327, 741, 730, 710, 970, 598, 571, -56, -351, 779, 928, 581, 393, 554, 856])
    h.remove_min()
    print(h)


    # print("\nPDF - build_heap example 1")
    # print("--------------------------")
    # da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    # da.set_at_index(0, 500)
    # print(da)
    # print(h)
