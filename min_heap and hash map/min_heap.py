# Course: CS261 - Data Structures
# Assignment: 5
# Student: Ian Rolph
# Description: An implementation of a min heap using a DynamicArray.


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
        """
        Adds a given node to the MinHeap, percolating it upwards until it reaches its place.
        """
        self.heap.append(node)
        i = self.heap.length() - 1
        while i > 0:
            if self.heap.get_at_index(int((i - 1) / 2)) > self.heap.get_at_index(i):
                self.heap.swap(i, int((i - 1) / 2))
            i = int((i-1) / 2)

    def get_min(self) -> object:
        """
        Returns the minimum value of the MinHeap.
        """
        if self.heap.length() == 0:
            raise MinHeapException
        return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Removes the minimum value, or the root of the MinHeap, and replaces it
        with the next lowest value, then returns the value that was removed.
        """
        if self.heap.length() == 0:
            raise MinHeapException
        return_val = self.heap.get_at_index(0)
        if self.heap.length() > 1:
            self.heap.set_at_index(0, self.heap.pop())
            i = 0
            while (2 * i + 1 < self.heap.length() and 2 * i + 2 < self.heap.length()) or (2 * i + 1 < self.heap.length() and 2 * i + 2 >= self.heap.length()):
                left_index = 2 * i + 1
                right_index = 2 * i + 2
                if (2 * i + 1 < self.heap.length() and 2 * i + 2 < self.heap.length()):     # both children are in range
                    if self.heap.get_at_index(left_index) >= self.heap.get_at_index(i) and self.heap.get_at_index(right_index) >= self.heap.get_at_index(i):
                        break
                    if self.heap.get_at_index(left_index) <= self.heap.get_at_index(right_index):
                        if self.heap.get_at_index(left_index) < self.heap.get_at_index(i):
                            self.heap.swap(i, left_index)
                            i = left_index
                        else:
                            break
                    elif self.heap.get_at_index(left_index) > self.heap.get_at_index(right_index):
                        if self.heap.get_at_index(right_index) < self.heap.get_at_index(i):
                            self.heap.swap(i, right_index)
                            i = right_index
                        else:
                            break
                    else:
                        print("what 2")
                        break
                elif (2 * i + 1 < self.heap.length() and 2 * i + 2 >= self.heap.length()):  # only left is in range
                    if self.heap.get_at_index(left_index) <= self.heap.get_at_index(i):
                        self.heap.swap(i, left_index)
                        i = left_index
                    else:
                        break
                else:
                    break
        else:
            self.heap.pop()
        return return_val



    def build_heap(self, da: DynamicArray) -> None:
        """
        Given a DynamicArray, changes the MinHeap's internal array
        to a heap made of the values in the input DynamicArray.
        """
        new_array = DynamicArray()
        for i in da:
            new_array.append(i)
        place = int((new_array.length() / 2) - 1)
        while place >= 0:
            left_index = 2 * place + 1
            right_index = 2 * place + 2
            if right_index >= new_array.length() and left_index < new_array.length():       # only left index
                if new_array.get_at_index(left_index) < new_array.get_at_index(place):     # swap
                    new_array.swap(place, left_index)
                    place = left_index
                    continue
                else:
                    place -= 1
                    continue
            elif right_index >= new_array.length() and left_index >= new_array.length():
                place -= 1
                continue
            else:
                if new_array.get_at_index(left_index) <= new_array.get_at_index(right_index): # left is less/equal to right
                    if new_array.get_at_index(left_index) < new_array.get_at_index(place):
                        new_array.swap(place, left_index)
                        place = left_index
                        continue
                    else:
                        place -= 1
                        continue
                else:                                                           # right is less than left
                    if new_array.get_at_index(right_index) < new_array.get_at_index(place):
                        new_array.swap(place, right_index)
                        place = right_index
                        continue
                    else:
                        place -= 1
                        continue
        self.heap = new_array
        



        
            
            

# BASIC TESTING
# if __name__ == '__main__':

    # print("\nPDF - add example 1")
    # print("-------------------")
    # h = MinHeap()
    # print(h, h.is_empty())
    # for value in range(300, 200, -15):
    #     h.add(value)
    #     print(h)

    # print("\nPDF - add example 2")
    # print("-------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
    #     h.add(value)
    #     print(h)

    # print("\nPDF - add example 3")
    # print("-------------------")
    # h = MinHeap()
    # print(h)
    # for value in [1, 3, 4, 5, 7, 1, 6, 4, 1, 2, 3]:
    #     h.add(value)
    #     print(h)


    # print("\nPDF - get_min example 1")
    # print("-----------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # print(h.get_min(), h.get_min())


    # print("\nPDF - remove_min example 1")
    # print("--------------------------")
    # h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    # while not h.is_empty():
    #     print(h, end=' ')
    #     print(h.remove_min())

    # print("\nremove_min example 2")
    # print("--------------------------")
    # h = MinHeap([-1000, -994, -963, -986, -993, -925, -893, -980, -926, -970, -976, -919, -923, -844, -833, -916, -967, -873, -831, -905, -893, -883, -887, -808, -607, -767, -897, -795, -691, -814, -827, -632, -870, -909, -886, -547, -582, -773, -752, -493, -680, -560, -750, -657, -575, -809, -834, -567, -634, -380, -547, -500, -688, -103, -551, -752, -232, -89, -378, -675, -728, -476, -691, -529, -621, -663, -722, -592, -873, -865, -831, -354, -4, -182, -375, -630, -560, -349, 215, 8, -295, -369, -278, -476, -59, -370, -738, -199, 220, -145, -128, -123, -350, -601, -695, -299, -434, 120, -165, 428, 206, 337, 275, -465, -299, -188, -622, 238, 18, -548, 701, -155, -314, -101, -224, 125, -53, 32, 325, -206, -242, -357, -125, 168, -180, -403, 371, -394, -529, -347, -271, -307, -560, -602, 149, 716, -291, -683, -761, -195, -10, -582, -171, -212, 81, 456, 39, -152, -165, -93, 283, -373, -234, -405, -307, 82, -336, 365, 515, 450, 36, -166, -286, -216, -265, 167, 416, 770, 133, -58, 72, 24, -363, -219, -716, 27, 94, 373, 610, 967, 192, 457, 542, 646, 158, 24, -80, -499, 675, 967, -685, 819, -179, 214, -230, 606, 638, 406, 983, 904, 728, 796, 692, 700, 420, 504, 948, 830, 226, 979, 212, -133, 539, 547, 571, 824, 401, 957, 169, -211, -416, 933, 918, 866, 650, -43, 736, 439, 42, 716, 560, 792, 675, 938, 237, 939, 652, 785, 817, 798, 555, 449, 121, 651, 399, 567, 63, 743, 929, 724, 567, 667, -279, 706, 588, 845, 155, 166, -514, 346, 878, 715, 601, 504, -97, -181, 958, 71, -4, 383, 214, 943, 989, 671, 406, 724, -208, 19, 474, 984, -17, 513, 325, 622, -151, 426, 945, 689, -111, 454, 656, 605, 730, 632, 345, 464, 222, 503, 869, 683, 451, 449, 592, 970, 164, 33, 156, 853, -13, -103, -278, 969, 361, 83, -320, 884, 644, 566, 651, 909, 452, 897, 292, 594, 309, 867, 311, 720, 447, 627, 981, 926, 547, 830, 691, 865, 909, 415, 168, 363, 950, 928, 578, 338, 800, -333, 579, 821, 217, 277, -673, 678])
    # while not h.is_empty():
    #     print(h, end=' ')
    #     print(h.remove_min())
    
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

    # print("\nPDF - build_heap example 2")
    # print("--------------------------")
    # da = DynamicArray([32, 12, 2, 8, 16, 20, 24, 40, 4])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    # da.set_at_index(0, 500)
    # print(da)
    # print(h)

    # print("\nPDF - build_heap example 2")
    # print("--------------------------")
    # da = DynamicArray([-779, -534, -377, -847, 407, 616, -788, -587, 612, -679, 448, 510, -133, -418, -496, 605, 911, 925, 691, 298, -757, 289, 323, 36, -755, 273, 2, 666, 528, 328, -280, -327, -474, -765, 140, -719, 933, 717, -647, -271, 814, -141, 899, 759, -971, -323, -159, -935, -642, -586, -686, -590, 241, -233, 460, -346, -335, 669, 682, -426, 766, 413, 647, 184, 309, 742, -34, 363, -586, -642, -126, 274, -825, 859, -96, 127, 448, -326, -692, -37, 24, -458, 945, -589, 838, 768, 196, 636, -485, -922, -509, 804, -914, -307, 321, -903, 99, 767, -217, -413, 405, 413, 396, 845, 949, -798, -173, 138, -613, -306, -638, -612, 679, -616, 165, -34, 915, -700, 665, -760, 784, -406, 947, -595, 47, -114, 551, 746, 919, 941, 709, 249, 92, -615, 607, -864, -758, -619, -127, 699, -857, -5, 629, 531, 663, -804, 226, -399, -474, 426, -968, -482, 373, -518, -75, -259, -985, -706, 576, 688, -34, -520, 32, 851, -575, -653, 54, 488, 890, -613, -332, -380, -637, 525, -121, 497, -789, 33, -689, 743, 165, -811, -605, 795, -105, 756, -971, 314, -99, -412, -159, 587, -382, 231, -544, 832, 384, -512, 847, 99, -683, 529, -567, -52, 69, 782, 733, -3, 432, -10, -453, -77, -195, -407, 104, 270, -917, -88, 390, -32, -157, 591, -550, -202, -310, 852, -773, 575, 909, -604, -641, -590, -560, -257, 91, 265, -982, -268, -301, 440, -820, -962, 512, 631, 991, 223, 644, -603, -168, 742, 212, 882, -887, -341, -327, 68, -969, -367, 56, 978, -711, -5, 628, -349, -389, 442, 5, 643, -612, -106, 35, -363, 95, -135, -857, -872, -120, 4, -16, -471, -56, -807, -409, 619, 498, 770, 588, 714, 946, -549, 963, -558, 3, -73, 971, -391, -839, -72, -967, 219, -149, -586, -417, 666, 508, 898, 117, 850, 604, 805, 997, -976, 681, -911, -518, -121, 417, 647, -611, 170, -883, -84, -642, 848, 418, -923, 758, -956, -341, 783])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    # da.set_at_index(0, 500)
    # print(da)
    # print(h)