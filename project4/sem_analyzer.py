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
            node = self.tail.prev
            self.tail.prev = self.tail.prev.prev
            self.tail.prev.next = self.tail
            return node

    def last(self):
        return self.tail.prev

class ProgramScope:
    list = None
    current_scope = None
    current_func = None
    closed_scopes = None

    class SymbolTable:
        func_id = None
        table = {}

        def append(self, key, type):
            self.table.update({key: type})

        def update(self, key, type):
            self.table.update({key: type})

        def get_type(self, id):
            return self.table[id]

        def get(self, id):
            return self.table[id] if self.has_id(id) else None

        def has_id(self, id):
            if id in self.table:
                return True
            else:
                return False

        def get_keys(self):
            return self.table.keys()

    def __init__(self):
        self.list = DoubleLinkedList()
        self.current_scope = self.SymbolTable()
        self.list.add_last(self.current_scope)

    # ----add new scope to program -----------
    def new_scope(self, function):
        if function is not None:
            self.current_func = function
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

    def pop_scope(self):
        node = self.list.remove()
        self.closed_scopes.append(node.data.id)
        return node.data

    def get_last_scope(self):
        return self.closed_scopes.pop()

    def get_keys(self):
        return self.current_scope.get_keys()


# ---------- semantic classes ------------------------------

def reject(string):
    print('rejected on '+ string)
    return False

class Program:
    prgm_valid = True
    dec_list = None
    PS = ProgramScope()

    def reject(self):
        self.prgm_vlalid = False

    def declaration_list(self):
        self.dec_list = DeclarationList()
        return self.dec_list

    def verify(self):
        last_scope = self.PS.scope_track.pop()
        if last_scope.func_id == 'main':
            if self.dec_list.verify():
                return True
        return reject('Program')

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

    def verify(self):
        for dec in self.declarations:
            if dec.verify:
                continue
            else:
                return reject('DecList')
        if self.dec_list_prime is not None:
            if self.dec_list_prime.verify is True:
                return True
            else:
                return reject('DecList')
        return True

class Declaration(DeclarationList):
    pass
    type = None
    id = None
    dec_prime = None

    def init_dec_prime(self):
        self.dec_prime = DeclarationPrime()
        return self.dec_prime

    def verify(self):
        if self.PS.current_scope_has_id(self.id):
            return reject('Declaration')
        else:
            self.PS.add(self.id, self.type)
            return True
        if not self.dec_prime.verify:
            return reject('Declaration')

    def assign_type(self, type):
        self.type = type

    def assign_id(self, id):
        self.id = id

class TypeSpecifier:
    def __init__(self, type):
        self.type = type

class DeclarationPrime(Declaration):
    pass
    var = None
    func = None

    def verify(self, id, type):
        if self.var is not None:
            if self.var.verify(id, type):
                return True
            else:
                return False
        elif self.func is not None:
            if self.func.verify(id, type):
                return True
            else:
                return False

    def init_var(self):
        self.var = VarDec(self.type, self.id)
        return self.var

    def init_function(self):
        self.func = FuncDec(self.type, self.id)
        return self.func

class FuncDec(Program):
    compound_stmt = None
    function = None

    def __init__(self, type, id):
        self.function = Function(type, id)

    def verify(self):
        if self.function.is_valid:
            if self.compound_stmt.verify():
                return True
        else:
            return reject('FuncDec')

    def add_param(self, id, type):
        self.function.add_param(id, type)

    def add_scope(self):
        self.scope = self.PS.new_scope(self.function)

    def new_stmt(self):
        self.compound_stmt = CompoundStmt()
        return self.compound_stmt

    def new_function(self):
        self.function = Function(self.type, self.id)
        return self.function

class Function(Program):
    is_valid = True
    type = None
    id = None
    params = {}
    return_type = None

    def __init__(self, type, id):
        self.type = type
        self.id = id
        if not self.PS.has_id(id):
            self.PS.add(self.id, self.function)

    def add_param(self, id, type):
        if id not in self.params.keys() and 'void' not in self.params.keys():
            param = Params(type)
            self.params.update({id: param})
            return param
        else:
            self.is_valid = False
            return None

class Params(Function):
    type = None
    is_array = None
    def __init__(self, type):
        self.type = type

class Var(Program):
    is_valid = True
    type = None
    id = None

    def __init__(self, id, type):
        self.type = type
        self.id = id
        if type is not 'void':
            self.PS.add(id, self)
        else:
            self.is_valid = False

class Array(Program):
    is_valid = True
    size = None
    type = None
    id = None

    def __init__(self, id, type, size):
        self.type = type
        self.id = id
        self.size = int(size)
        if self.size <= 0 or type == 'void':
            self.is_valid = False
        else:
            self.PS.add(id, self)

class VarDec(Program):
    Var = None

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def new_var(self):
       self.Var = Var(self.id, self.type)

    def new_array(self, size):
        self.Var = Array(self.id, self.type, size)

    def verify(self, id, type):
        if Var.is_valid:
            return True
        else:
            return False

class CompoundStmt(Program):
    local_dec = None
    stmt_list = None

    def dec_local_var(self):
        self.local_dec = LocalDeclaration()
        return self.local_dec

    def init_stmt_list(self):
        self.stmt_list = StatementList()
        return self.stmt_list

class LocalDeclaration(Program):
    declarations = []

    def create_vardec(self, id, type):
        vardec = VarDec(id, type)
        self.declarations.append(vardec)
        return self.vardec

    def verify(self):
        for dec in self.declarations:
            if dec.verify:
                continue
            else:
                return reject('LocalDec')

class StatementList(CompoundStmt):
    stmt = None
    stmt_list = None

    def new_stmt(self):
        self.stmt = Statement()
        return self.stmt

    def new_stmt_list(self):
        self.stmt_list = StatementList()
        return self.stmt_list

    def verify(self):
        if self.stmt.verify():
            if self.stmt_list.verify():
                return True
        return reject('StmtList')

class Statement(Program):
    stmt = None

    def new_stmt(self, stmt):
        self.stmt = stmt
        return stmt

    def verify(self):
        if self.stmt.verify:
            return True
        else:
            return reject('Statment')

class IfStmt(Statement):
    pass

class WhileStmt(Statement):
    pass

class AssignStmt(Statement):
    pass

class ReturnStmt(Statement):
    pass
    exp_stmt = None

    def new_exp_stmt(self):
        self.exp_stmt = Expression()
        return self.exp_stmt

    def verify(self):
        result = self.exp_stmt.evaluate()
        if result == False:
            return False
        if result == self.PS.current_func.type:
            return True
        else:
            return reject('ReturnStmt')

class Expression(Program):
    pass
    exp = None

    def verify(self):
        if self.exp.verify():
            return True
        else:
            return reject('Expression')

    def new_num_exp(self, num):
        self.exp = NumExp(num)
        return self.exp

class NumExp(Expression):
    pass
    num = 'int'
    term = None
    add_exp = None
    sim_exp = None

    def new_term(self):
        self.term = Term()
        return self.term

    def new_add_exp(self):
        self.add_exp = AddExp()
        return self.add_exp

    def __init__(self, num):
        self.number = num

    def evaluate(self):
        if self.term is not None:
            if self.term.eval() != self.type:
                self.reject()
        if self.add_exp is not None:
            if self.add_exp.eval() != self.type:
                self.reject()
        if self.sim_exp is not None:
            if self.sim_exp.eval != self.type:
                self.reject()
        return self.type

class RefExp(Expression):
    pass
    id = None
    exp = None

    def __init__(self, id):
        self.id = id

    def evaluate(self):
        return self.exp.evaluate()

    def new_array_exp(self):
        self.exp = ArrayExp(self.id)
        return self.exp

    def new_var_exp(self):
        self.exp = VarExp(self.id)
        return self.exp

    def new_func_exp(self):
        self.exp = FunExp(self.id)
        return self.exp

class ArrayExp(Expression):
    pass
    id = None
    exp = None

    def __init__(self, id):
        self.id = id

    def new_exp(self):
        self.exp = Expression()
        return self.exp

    def evaluate(self):
        if self.PS.has_id(self.id):
            arr = self.PS.get(self.id)
        else:
            return None
        if arr.type == self.exp.evaluate():
            return arr.type
        else:
            return None

class VarExp(Expression):
    pass
    var = None
    def __init__(self, id):
        self.id = id

    def evaluate(self):
        if self.PS.has(self.id):
            self.var = self.PS.get(id)
        else:
            return None
        return self.var.type


class FunExp(Expression):
    pass
    func = None
    args = None
    term = None
    add_exp = None
    sim_exp = None

    def __init__(self, id):
        self.id = id

    def evaluate(self):
        if self.

class AddExp(Program):
    term = None
    add_exp_prime = None

    def evaluate(self):
        type1 = self.term.evaluate() if self.term is not None else None
        type2 = self.add_exp_prime.evaluate() if self.add_exp_prime is not None else None

        if type1 is not None and type2 is not None:
            return None
        if type1 == type2:
                return type1
        return None

class Term(Program):
    factor = None
    term_prime = None

    def new_factor(self):
        self.factor = Factor()

    def new_term(self):
        self.term_prime = Term()
        return self.term_prime

    def evaluate(self):
        if self.factor is None:

        self.eval_type = self.factor.evaluate()
        if self.eval_type == self.term_prime.evaluate():
            return self.eval_type
        elif:
            return None

class Factor(Program):
    factor = None

    def factor(self, fact):
        self.factor = fact

    def evaluate(self):
        return self.factor.evaluate()

class Num(Factor):
    pass
    def evaluate(self):
        self.type = 'int'
        return self.type

class Exp(Factor):
    exp = None

    def new_exp(self):
        self.exp = Expression()
        return self.exp

    def evaluate(self):
        return self.exp.evaluate()

class FunCall(Factor):
    pass
    id = None
    args = None
    Func = None

    def __init__(self, id):
        self.id = id

    def verify(self):
        if self.PS.has_id(self.id):
            self.func = self.PS.get(self.id)
        else:
            return None
        if len(self.args) == len(self.func.params):
            return self.func.type
        else:
            return None

class VarCall(Factor):
    pass
    id = None

    def __init__(self, id):
        self.id = id

    def evaluate(self):
        if self.PS.has_id(self.id):
            var = self.PS.get(self.id)
            return var.type
        else:
            return None

class ArrayCall(Factor):
    pass
    id = None
    arr = None
    exp = None
    index = None

    def __init(self, id):
        self.id = id

    def new_exp(self):
        self.exp = Expression()
        return self.exp

    def verify(self):
        if self.PS.has_id(self.id):
            self.arr = self.PS.get(self.id)
        else:
            return None
        index = self.exp.evaluate()
        if index == self.arr.type:
            return self.arr.type



