"""
This script should sort the blocks in a crate based on their priority. Ideally,
when the rover reaches the crate, it wants to identify which piece of rubbish is
the most important, but the blocks are placed randomly by the robotic arm so the
rover has to 'analyse' and decide which item to carry.

For example, a battery or toxic waste would be of priority 1, and a crisp packet 5.
The priorities are a virtual representation of the type of item.

The blockdict has items in the format {block_name: priority}

Merge sort is a divide and conquer algorithm with best and worst case O(nlogn)
Source of merge sort implementation: https://www.w3schools.com/dsa/dsa_algo_mergesort.php
"""

class MergeSort:
    def __init__(self, blockdict):
        self.blocks = blockdict

    def get_sorted(self):
        items = list(self.blocks.items()) # converts to list of tuples
        return dict(self.merge_sort(items)) # new sorted dictionary

    def merge_sort(self, items):
        length = len(items)
        if length <=1:
            return items
        
        middle = length//2 # middle index to split the list by
        left = self.merge_sort(items[:middle])
        right = self.merge_sort(items[middle:])

        return self.merge(left, right)

    def merge(self, l, r):
        i = 0
        j = 0
        sorted_list = []

        while i<len(l) and j<len(r):
            if l[i][1] < r[j][1]: # compare the priorities
                sorted_list.append(l[i])
                i += 1
            else:
                sorted_list.append(r[j])
                j += 1
        
        sorted_list.extend(l[i:])
        sorted_list.extend(r[j:])
        return sorted_list


# Test data:
#blockdict = {
#    'block1': 4,
#    'block2': 2,
#    'block3': 3,
#    'block4': 1
#}

#sorted_dict = MergeSort(blockdict).get_sorted()
#print(blockdict)
#print(sorted_dict)
