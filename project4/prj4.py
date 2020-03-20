from scanner import *
from sem_analyzer import *
import sys


class Parser:
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

    # ----- parser functions --------

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens[self.count]

    def accept(self, token):
        self.count += 1
        self.current_token = self.tokens[self.count]

    def reject(self):
        self.result = False

    def program(self):
        program = Program()
        self.declaration_list(program.declaration_list())
        if self.current_token.type == '$':
            return
        else:
            self.reject

    def declaration_list(self, dec_list):
        self.declaration(dec_list.init_declaration())
        self.declaration_list_prime(dec_list.init_dec_list_prime())

    def declaration_list_prime(self, dec_list_prime):
        if self.current_token.type in ['int', 'void']:
            self.declaration(dec_list_prime.init_declaration())
            self.declaration_list_prime(dec_list_prime.init_dec_list_prime())

    def type_specifier(self):
        if self.current_token.type in ['int', 'void']:
            type_spec = TypeSpecifier(self.current_token.type)
            self.accept(self.current_token)
            return type_spec.type
        else:
            self.reject

    def declaration(self, declaration):
        declaration.assign_type(self.type_specifier())
        if self.current_token.type == 'ID':
            declaration.assign_id(self.current_token.value)
            self.accept('ID')
            if not declaration.verify(): self.reject()
            self.declaration_prime(declaration.init_dec_prime())
        else:
            self.reject

    def var_declaration(self, var_dec):
        if self.current_token.type == ';':
            self.accept(';')
            if not var_dec.verify(): self.reject()
            return
        elif self.current_token.type == '[':
            self.accept('[')
            if self.current_token.type == 'NUM':
                var_dec.array_size = self.current_token.value
                self.accept('NUM')
                if self.current_token.type == ']':
                    self.accept(']')
                    if self.current_token.type == ';':
                        self.accept(';')
                        if not var_dec.verify(): self.reject()
                        return
        self.reject()

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

    def declaration_prime(self, dec_prime):
        if self.current_token.type in self.var_declaration_first:
            self.var_declaration(dec_prime.init_var())
        elif self.current_token.type == '(':
            self.accept('(')
            self.params(dec_prime.init_function())
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

    def params(self, function):
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
    # file = sys.argv[1]
    file = input()
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
