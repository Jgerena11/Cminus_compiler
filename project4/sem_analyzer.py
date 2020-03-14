class SemanticAnalyzer:
    class SymbolTable:
        table = {}

        def append(self, key, type):
            self.table.update({key: type})

        def update(self, key, type):
            self.table.update({key: type})

    class DoubleLinkedList:
        class Node:
            def __init__(self, prev, next, data):
                self.prev = prev
                self.next = next
                self.data = data

        def __init__(self):
            self.head = self.Node(None, None, None)
            self.tail = self.Node(None, None, None)

        def add_last(self, data):
            if self.head.next == None and self.tail.prev == None:
                node = self.Node(self.head, self.tail, data)
                self.head.next = node
                self.tail.prev = node
            else:
                node = self.Node(self.tail.prev, self.tail, data)
                self.tail.prev.next = node
                self.tail.prev = node

        def remove(self):
            if self.tail.prev == self.head.next:
                self.head.next = self.tail
                self.tail.prev = self.head
            else:
                self.tail.prev = self.tail.prev.prev
                self.tail.prev.next = self.tail

    current_table = SymbolTable()
    list = DoubleLinkedList()
    list.add_last(current_table)

    class Declaration:
        type = None
        id = None

        def __init__(self, type, id):
            self.type = type
            self.id = id

        def semantic_check(self):



