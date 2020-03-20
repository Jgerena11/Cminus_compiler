class ProgramScope:
    list = None
    current_scope = None

    class SymbolTable:
        table = {}

        def append(self, key, type):
            self.table.update({key: type})

        def update(self, key, type):
            self.table.update({key: type})

        def get_type(self, id):
            return self.table[id]

        def get(self, id):
            return self.table[id]

        def has_id(self, id):
            if id in self.table:
                return True
            else:
                return False

    class DoubleLinkedList:
        head = None
        tail = None

        class Node:
            prev = None
            next = None

            def __init__(self, prev, next, data):
                self.prev = prev
                self.next = next
                self.scope = data

        def __init__(self):
            self.head = self.Node(None, None, None)
            self.tail = self.Node(None, None, None)

        def add_last(self, new_data):
            if self.head.next is None and self.tail.prev is None:
                node = self.Node(self.head, self.tail, new_data)
                self.head.next = node
                self.tail.prev = node
            else:
                node = self.Node(self.tail.prev, self.tail, new_data)
                self.tail.prev.next = node
                self.tail.prev = node

        def remove(self):
            if self.tail.prev == self.head.next:
                self.head.next = self.tail
                self.tail.prev = self.head
            else:
                self.tail.prev = self.tail.prev.prev
                self.tail.prev.next = self.tail

        def last(self):
            return self.tail.prev

    def __init__(self):
        self.list = self.DoubleLinkedList()
        self.current_scope = self.SymbolTable()
        self.list.add_last(self.current_scope)

    #----add new scope to program -----------
    def new_scope(self):
        table = self.SymbolTable()
        self.current_scope = table
        self.list.add_last(table)

    def get_scope(self, id):
        node = self.list.last()
        while node is not self.list.head:
            if node.table.has_id(id):
                return node.table
            else:
                node = node.prev
        return None

    #----- check if current scope has id --------
    def current_scope_has_id(self, id):
        if self.current_scope.has_id(id):
            return True
        else:
            return False

    # check for id is reachable
    def has_id(self, id):
        scope = self.get_scope(id)
        if scope.has_id(id):
            return True
        else:
            return False

    #returns the type object of the id
    def get(self, id):
        scope = self.get_scope(id)
        return scope.get(id)

    #update type of id in the program
    def update(self, id, data):
        scope = self.get_scope(id)
        scope.update(id, data)

    def add(self, id, type):
        self.current_scope.append(id, type)









