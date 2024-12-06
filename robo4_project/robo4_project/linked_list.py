class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self) -> bool:
        return self.head is None

    def insert(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def next(self, curr_node):
        if curr_node is None:
            return self.head
        else:
            return curr_node.next