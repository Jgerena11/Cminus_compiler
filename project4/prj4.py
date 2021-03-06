from scanner import *
import sys

class DoubleLinkedList:

    class Node:
        def __init__(self, prev, next, data):
            self.prev = prev
            self.next = next
            self.data = data

    def __init__(self):
        self.head = self.Node(None, None, None)
        self.tail = self.Node(None, None, None)

    def append(self, data):
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


class SymbolTable:
    table = {}

    def append(self, key, type):
        self.table.update({key: type})

    def update(self, key, type):
        self.table.update({key: type})

class Parser:

    list = DoubleLinkedList()
    table = SymbolTable()
    list.append(table)

    var_declaration_first = [';', '[']
    type_specifier_first = ['int', 'void']
    compound_stmt_first = ['{']
    factor_first = ['(', 'ID', 'NUM']
    expression_stmt_first = ['(', 'ID', 'NUM', ';']
    expression_first = ['(', 'ID', 'NUM']
    expression_double_prime_first = ['=', '*', '/', '+', '-', '<=', '>', '<', '>=', '==', '!=']
    statement_first = ['(', 'ID', 'NUM', ';', 'if', 'while', 'return', '{']

    count = 0
    result = True

    def compare_type(self, a, b):
        if type(a) is not type(b):
            result = False
            return False
        else: return True

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens[self.count]

    def program(self):
        self.declaration_list()
        if self.current_token.type == '$':
            return
        else:
            self.result = False

    def declaration_list(self):
        self.declaration()
        self.declaration_list_prime()

    def accept(self, token):
        self.count += 1
        self.current_token = self.tokens[self.count]

    def declaration_list_prime(self):
        if self.current_token.type in ['int', 'void']:
            self.declaration()
            self.declaration_list_prime()

    def type_specifier(self):
        if self.current_token.type in ['int', 'void']:
            self.accept(self.current_token)
        else:
            self.result = False

    def declaration(self):
        self.type_specifier()
        if self.current_token.type =='ID':
            self.accept('ID')
            self.declaration_prime()
        else:
            self.result = False


    def var_declaration(self):
        if self.current_token.type == ';':
            self.accept(';')
            return
        elif self.current_token.type == '[':
            self.accept('[')
            if self.current_token.type == 'NUM':
                self.accept('NUM')
                if self.current_token.type == ']':
                    self.accept(']')
                    if self.current_token.type == ';':
                        self.accept(';')
                        return
        self.result = False

    def statement_list(self):
        if self.current_token.type in self.statement_first:
            self.statement()
            self.statement_list()

    def local_declarations(self):
        if self.current_token.type in ['int', 'void']:
            self.accept(self.current_token)
            if self.current_token.type == 'ID':
                self.accept('ID')
                self.var_declaration()
                self.local_declarations()


    def compound_stmt(self):
        if self.current_token.type == '{':
            self.accept('{')
            self.local_declarations()
            self.statement_list()
            if self.current_token.type == '}':
                self.accept('}')
            else:
                self.result = False
        else:
            self.result = False

    def declaration_prime(self):
        if self.current_token.type in self.var_declaration_first:
            self.var_declaration()
        elif self.current_token.type == '(':
            self.accept('(')
            self.params()
            if self.current_token.type == ')':
                self.accept(')')
                self.compound_stmt()

    def param_prime(self):
        if self.current_token.type == '[':
            self.accept('[')
            if self.current_token.type == ']':
                self.accept(']')
            else:
                self.result = False

    def param(self):
        self.type_specifier()
        if self.current_token.type == 'ID':
            self.accept('ID')
            self.param_prime()

    def param_list_prime(self):
        if self.current_token.type == ',':
            self.accept(',')
            self.param_list()

    def param_list(self):
        self.param()
        self.param_list_prime()

    def params(self):
        if self.current_token.type == 'void':
            self.accept('void')
            self.params_prime()
        elif self.current_token.type == 'int':
            self.accept('int')
            if self.current_token.type == 'ID':
                self.accept('ID')
                self.param_prime()
                self.param_list_prime()
        else:
            self.result = False

    def params_prime(self):
        if self.current_token.type == 'ID':
            self.accept('ID')
            self.param_prime()
            self.param_list_prime()

    def statement(self):
        if self.current_token.type in self.expression_stmt_first:
            self.expression_stmt()
        elif self.current_token.type in self.compound_stmt_first:
            self.compound_stmt()
        elif self.current_token.type == 'if':
            self.selection_stmt()
        elif self.current_token.type == 'while':
            self.iteration_stmt()
        elif self.current_token.type == 'return':
            self.return_stmt()
        else:
            self.result = False

    def selection_stmt(self):
        if self.current_token.type == 'if':
            self.accept('if')
            if self.current_token.type == '(':
                self.accept('(')
                self.expression()
                if self.current_token.type == ')':
                    self.accept(')')
                    self.statement()
                    self.selection_stmt_prime()
                else:
                    self.result = False
            else:
                self.result = False

    def selection_stmt_prime(self):
        if self.current_token.type == 'else':
            self.accept('else')
            self.statement()

    def iteration_stmt(self):
        if self.current_token.type == 'while':
            self.accept('while')
            if self.current_token.type == '(':
                self.accept('(')
                self.expression()
                if self.current_token.type == ')':
                    self.accept(')')
                    self.statement()
                else:
                    self.result = False
            else:
                self.result = False

    def return_stmt(self):
        if self.current_token.type == 'return':
            self.accept('return')
            self.return_stmt_prime()

    def return_stmt_prime(self):
        if self.current_token.type == ';':
           self.accept(';')
        elif self.current_token.type in self.expression_first:
            self.expression()
            if self.current_token.type == ';':
                self.accept(';')
            else:
                self.result = False
        else:
            self.result = False


    def expression_stmt(self):
        if self.current_token.type in self.expression_first:
            self.expression()
            if self.current_token.type == ';':
                self.accept(';')
            else:
                self.result = False
        elif self.current_token.type == ';':
            self.accept(';')
        else:
            self.result = False

    def expression(self):
        if self.current_token.type == '(':
            self.accept('(')
            self.expression()
            if self.current_token.type == ')':
                self.accept(')')
                self.term_prime()
                self.additive_expression_prime()
                self.simple_expression()
            else:
                self.result = False
        elif self.current_token.type == 'ID':
            self.accept('ID')
            self.expression_prime()
        elif self.current_token.type == 'NUM':
            self.accept('NUM')
            self.term_prime()
            self.additive_expression_prime()
            self.simple_expression()
        else:
            self.result = False

    def expression_prime(self):
        if self.current_token.type == '[':
            self.accept(self.current_token)
            self.expression()
            if self.current_token.type == ']':
                self.accept(']')
                self.expression_double_prime()
            else:
                self.result = False
        elif self.current_token.type == '(':
            self.accept('(')
            self.args()
            if self.current_token.type == ')':
                self.accept(')')
                self.term_prime()
                self.additive_expression_prime()
                self.simple_expression()
            else:
                self.result = False
        elif self.current_token.type in self.expression_double_prime_first:
            self.expression_double_prime()

    def expression_double_prime(self):
        if self.current_token.type == '=':
            self.accept(self.current_token)
            self.expression()
        else:
            self.term_prime()
            self.additive_expression_prime()
            self.simple_expression()

    def simple_expression(self):
        if self.current_token.type in ['<=', '<', '>', '>=', '==', '!=']:
            self.accept(self.current_token)
            self.additive_expression()

    def relop(self):
        r = ['<=', '<', '>', '>=', '==', '!=']
        if self.current_token.type in r:
            self.accept(self.current_token.type)
        else:
            self.result = False

    def additive_expression(self):
        self.term()
        self.additive_expression_prime()

    def additive_expression_prime(self):
        if self.current_token.type in ['+', '-']:
            self.accept(self.current_token)
            self.term()
            self.additive_expression_prime()

    def term(self):
        self.factor()
        self.term_prime()

    def term_prime(self):
        if self.current_token.type in ['*', '/']:
            self.accept(self.current_token.type)
            self.factor()
            self.term_prime()

    def factor(self):
        if self.current_token.type == '(':
            self.accept(self.current_token)
            self.expression()
            if self.current_token.type == ')':
                self.accept(self.current_token)
            else:
                self.result = False
        elif self.current_token.type == 'ID':
            self.accept(self.current_token)
            self.factor_prime()
        elif self.current_token.type == 'NUM':
            self.accept(self.current_token)
        else:
            self.result = False

    def factor_prime(self):
        if self.current_token.type == '[':
            self.accept(self.current_token)
            self.expression()
            if self.current_token.type == ']':
                self.accept(self.current_token)
            else:
                self.result = False
        elif self.current_token.type == '(':
            self.accept(self.current_token)
            self.args()
            if self.current_token.type == ')':
                self.accept(self.current_token)
            else:
                self.result = False

    def args(self):
        if self.current_token.type in self.expression_first:
            self.expression()
            self.arg_list()

    def arg_list(self):
        if self.current_token.type == ',':
            self.accept(self.current_token)
            self.expression()
            self.arg_list()

try:
    file = sys.argv[1]
    f = open(file, 'r')
    scanner = Scanner(f)
    scanner.run_scanner()
    parse = Parser(scanner.tokens)
    parse.program()
    if parse.result == True:
        sys.stdout.write('ACCEPT')
    else:
        sys.stdout.write('REJECT')
    f.close()
except IOError:
    print('File not accessible')