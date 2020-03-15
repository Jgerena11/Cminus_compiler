class DoubleLinkedList:
    class Node:
        def __init__(self, prev, next, table):
            self.prev = prev
            self.next = next
            self.table = table

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

class SemanticAnalyzer:
    list = DoubleLinkedList
    current_table = None

    class SymbolTable:
        table = {}

        def append(self, key, type):
            self.table.update({key: type})

        def update(self, key, type):
            self.table.update({key: type})

        def get_type(self, id):
            return self.table[id]

    def get_type(self, id):
        node = list.tail
        while node is not list.head:
            if node.table[id]:
                return node.table.get_type
            else:
                node = node.prev
        return None

    def __init__(self):
        self.current_table = self.SymbolTable()
        self.list.add_last(self.current_table)

    def new_scope(self):
        table = self.SymbolTable()
        self.current_table = table
        self.list.add_last(table)
        
    class Declaration:
        type = None
        id = None
        declaration_prime = None

        def assign_type(self, type):
            self.type = type

        def assign_id(self, id):
            if self.table[id]:
                return False
            else:
                self.current_table.append(self.type, id)
                return True

        def get_type(self, id):
            if self.current_table

    class DeclarationPrime:
        var_declaration = None
        params = None

    class VarDeclaration:
        value = None

        def assign_value(self, value):
            if value.type = super().type:







