"""
MergeSort source: https://www.w3schools.com/dsa/dsa_algo_mergesort.php
"""

class Queue:
    def __init__(self):
        self.queue = []

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
            if l[i][0] > r[j][0]: # compare the priorities
                sorted_list.append(l[i])
                i += 1
            else:
                sorted_list.append(r[j])
                j += 1
        
        sorted_list.extend(l[i:])
        sorted_list.extend(r[j:])
        return sorted_list
    
    def add(self, item):
        self.queue.append(item)

    def pop(self):
        if not self.queue:
            return None
        return self.queue.pop(0)
    
    def size(self):
        return len(self.queue)