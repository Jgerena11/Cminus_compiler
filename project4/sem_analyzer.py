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

        def get_keys(self):
            return self.table.keys()

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

    # ----add new scope to program -----------
    def new_scope(self):
        table = self.SymbolTable()
        self.current_scope = table
        self.list.add_last(table)
        return table

    def get_scope(self, id):
        node = self.list.last()
        while node is not self.list.head:
            if node.table.has_id(id):
                return node.table
            else:
                node = node.prev
        return None

    # ----- check if current scope has id --------
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

    # returns the type object of the id
    def get(self, id):
        scope = self.get_scope(id)
        return scope.get(id)

    # update type of id in the program
    def update(self, id, data):
        scope = self.get_scope(id)
        scope.update(id, data)

    def add(self, id, type):
        self.current_scope.append(id, type)

    def print_keys(self):
        print(self.current_scope.get_keys())


# ---------- semantic classes ------------------------------

class Program:
    dec_list = None
    PS = ProgramScope()

    def declaration_list(self):
        self.dec_list = DeclarationList()
        return self.dec_list

class DeclarationList(Program):
    declarations = []
    dec_list_prime = None

    def init_declaration(self):
        declaration = Declaration()
        self.declarations.append(declaration)
        return declaration

    def init_dec_list_prime(self):
        dec_list_prime = DeclarationList()
        return dec_list_prime

class Declaration(DeclarationList):
    pass
    type = None
    id = None
    dec_prime = None

    def init_dec_prime(self):
        self.dec_prime = DeclarationPrime(self.type, self.id)
        return self.dec_prime

    def verify(self):
        if self.PS.current_scope_has_id(self.id):
            print('failed in declaration')
            return False
        else:
            self.PS.add(self.id, self.type)
            return True

    def assign_type(self, type):
        self.type = type

    def assign_id(self, id):
        self.id = id

class TypeSpecifier:
    def __init__(self, type):
        self.type = type

class DeclarationPrime(Declaration):
    pass
    var_declaration = None
    func_declaration = None

    def __init__(self, type, id):
        self.id = id
        self.type = type

    def init_var(self):
        self.var_declaration = VarDeclaration(self.type, self.id)
        return self.var_declaration

    def init_function(self):
        self.func_declaration = FunDeclaration(self.type, self.id)
        return self.func_declaration

class FunDeclaration(DeclarationPrime):
    type = None
    id = None
    params = {}
    scope = None
    return_type = None
    compound_stmt = None

    def __init__(self, type, id):
        self.type = type
        self.id = id
        self.PS.add(self.id, self)

    def verify(self):
        if self.type == 'void':
            if self.return_type is None:
                return True
            else:
                return False

    def add_param(self, id, type):
        if id not in self.params.keys() and 'void' not in self.params.keys():
            print(id)
            self.params.update({id: type})
            return True
        else:
            print(id)
            print('should fail here')
            return False

    def declare_var(self, type, id):
        self.var_declaration = VarDeclaration(type, id)
        return self.var_declaration

    def add_scope(self):
        self.scope = self.PS.new_scope()

class VarDeclaration(DeclarationPrime):
    has_array = False
    array = None
    array_size = None

    def __init__(self, type, id):
        self.type = type
        self.id = id

    def verify(self):
        if self.type == 'void':
            print('failed in var_declaration')
            return False
        self.PS.add(self.id, self)
        return True

class Expression(Program):
    operandA = None
    operandB = None
    op = None
    eval_type = None

    def assign_a(self, id):
        self.operandA = self.PS.get(id)

    def assign_b(self, id):
        self.operandB = self.PS.get(id)

    def assign_op(self, op):
        self.op = op

    def evaluation_type(self):
        if self.op == ''

    def add_expression

class Factor(Program):
    type = None
    id = None
