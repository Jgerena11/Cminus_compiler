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
        print('rejected on '+self.current_token.value)
        self.result = False

    def program(self):
        program = Program()
        self.declaration_list(program.declaration_list())
        if not program.verify(): self.reject()
        if self.current_token.type == '$':
            return
        else:
            self.reject()

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
            self.declaration_prime(declaration.init_dec_prime())
        else:
            self.reject

    def var_declaration(self, var_dec):
        var = var_dec.new_var()
        if self.current_token.type == ';':
            self.accept(';')
            return
        elif self.current_token.type == '[':
            self.accept('[')
            if self.current_token.type == 'NUM':
                var.add_array_size(self.current_token.value)
                self.accept('NUM')
                if self.current_token.type == ']':
                    self.accept(']')
                    if self.current_token.type == ';':
                        self.accept(';')
                        return
        self.reject()

    def statement_list(self, stmt_list):
        if self.current_token.type in self.statement_first:
            self.statement(stmt_list.new_stmt())
            self.statement_list(stmt_list.new_stmt_list)

    def local_declarations(self, local_dec):
        if self.current_token.type in ['int', 'void']:
            type = self.current_token.value
            self.accept(self.current_token)
            if self.current_token.type == 'ID':
                id = self.current_token.value
                local_dec.create_var(id, type)
                self.accept('ID')
                self.var_declaration(local_dec.create_vardec(id, type))
                self.local_declarations(local_dec)

    def compound_stmt(self, comp_stmt):
        if self.current_token.type == '{':
            self.accept('{')
            self.local_declarations(comp_stmt.dec_local_var())
            self.statement_list(comp_stmt.init_stmt_list())
            if self.current_token.type == '}':
                self.accept('}')
            else:
                self.reject()
        else:
            self.reject()

    def declaration_prime(self, dec_prime):
        if self.current_token.type in self.var_declaration_first:
            self.var_declaration(dec_prime.init_var())
        elif self.current_token.type == '(':
            self.accept('(')
            fun_dec = dec_prime.init_function()
            self.params(fun_dec.new_function())
            if self.current_token.type == ')':
                self.accept(')')
                fun_dec.add_scope()
                self.compound_stmt(fun_dec.new_stmt())

    def param_prime(self, param):
        if self.current_token.type == '[':
            self.accept('[')
            if self.current_token.type == ']':
                self.accept(']')
                param.is_array = True
            else:
                self.reject()

    def param(self, func):
        type = self.type_specifier()
        if self.current_token.type == 'ID':
            param = func.add_param(self.current_token.value, type)
            self.accept('ID')
            self.param_prime(param)

    def param_list_prime(self, function):
        if self.current_token.type == ',':
            self.accept(',')
            self.param_list(function)

    def param_list(self, function):
        self.param(function)
        self.param_list_prime(function)

    def params(self, function):
        if self.current_token.type == 'void':
            type = self.current_token.type
            function.add_param('void', 'void')
            self.accept('void')
            self.params_prime(function)
        elif self.current_token.type == 'int':
            type = 'int'
            self.accept('int')
            if self.current_token.type == 'ID':
                id = self.current_token.value
                param = function.add_param(type, id)
                self.accept('ID')
                self.param_prime(param)
                self.param_list_prime(function)
        else:
            self.reject()

    def params_prime(self, function):
        if self.current_token.type == 'ID':
            self.reject()
            self.param_prime(function)
            self.param_list_prime(function)

    def statement(self, stmt):
        if self.current_token.type in self.expression_stmt_first:
            self.expression_stmt(stmt.new_stmt(Expression()))
        elif self.current_token.type in self.compound_stmt_first:
            self.compound_stmt(stmt.new_stmt(CompoundStmt()))
        elif self.current_token.type == 'if':
            self.selection_stmt(stmt.new_stmt(IfStmt()))
        elif self.current_token.type == 'while':
            self.iteration_stmt(stmt.new_stmt(WhileStmt()))
        elif self.current_token.type == 'return':
            self.return_stmt(stmt.new_stmt(ReturnStmt()))
        else:
            self.reject()

    def selection_stmt(self, function):
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
                    self.reject()
            else:
                self.reject()

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
                    self.reject()
            else:
                self.reject()

    def return_stmt(self, return_stmt):
        if self.current_token.type == 'return':
            self.accept('return')
            self.return_stmt_prime(return_stmt)

    def return_stmt_prime(self, return_stmt):
        if self.current_token.type == ';':
            self.accept(';')
        elif self.current_token.type in self.expression_first:
            self.expression(return_stmt.new_exp_stmt())
            self.expression()
            if self.current_token.type == ';':
                self.accept(';')
            else:
                self.reject()
        else:
            self.reject()

    def expression_stmt(self):
        if self.current_token.type in self.expression_first:
            self.expression()
            if self.current_token.type == ';':
                self.accept(';')
            else:
                self.reject()
        elif self.current_token.type == ';':
            self.accept(';')
        else:
            self.reject()

    def expression(self):
        exp = Expression()
        if self.current_token.type == '(':
            self.accept('(')
            self.expression()
            if self.current_token.type == ')':
                self.accept(')')
                self.term_prime()
                self.additive_expression_prime()
                self.simple_expression()
            else:
                self.reject()
        elif self.current_token.type == 'ID':
            self.accept('ID')
            self.expression_prime()
        elif self.current_token.type == 'NUM':
            exp.typeA = 'int'
            self.accept('NUM')
            self.term_prime()
            self.additive_expression_prime()
            self.simple_expression()
            if not exp.verify():
                print('failed here')
                self.reject()
            return exp.eval_type
        else:
            self.reject()

    def expression_prime(self):
        if self.current_token.type == '[':
            self.accept(self.current_token)
            self.expression()
            if self.current_token.type == ']':
                self.accept(']')
                self.expression_double_prime()
            else:
                self.reject()
        elif self.current_token.type == '(':
            self.accept('(')
            self.args()
            if self.current_token.type == ')':
                self.accept(')')
                self.term_prime()
                self.additive_expression_prime()
                self.simple_expression()
            else:
                self.reject()
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
            self.reject()

    def additive_expression(self):
        self.term()
        self.additive_expression_prime()

    def additive_expression_prime(self):
        if self.current_token.type in ['+', '-']:
            self.accept(self.current_token)
            self.term()
            self.additive_expression_prime()

    def term(self, term):
        term = self.factor()
        self.term_prime()

    def term_prime(self, term):
        if self.current_token.type in ['*', '/']:
            self.accept(self.current_token.type)
            self.factor(term.new_factor())
            self.term_prime(term)

    def factor(self, factor):
        if self.current_token.type == '(':
            self.accept(self.current_token)
            factor.type = self.expression()
            if self.current_token.type == ')':
                self.accept(self.current_token)
            else:
                self.reject()
        elif self.current_token.type == 'ID':
            factor.var_type(self.current_token.value)
            self.accept(self.current_token)
            self.factor_prime(factor)
        elif self.current_token.type == 'NUM':
            factor.assign_primitive_value_int()
            self.accept(self.current_token)
        else:
            self.reject()

    def factor_prime(self):
        if self.current_token.type == '[':
            self.accept(self.current_token)
            self.expression()
            if self.current_token.type == ']':
                self.accept(self.current_token)
            else:
                self.reject()
        elif self.current_token.type == '(':
            self.accept(self.current_token)
            self.args()
            if self.current_token.type == ')':
                self.accept(self.current_token)
            else:
                self.reject()

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
    # file = input()
    f = open('test1.txt', 'r')
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
