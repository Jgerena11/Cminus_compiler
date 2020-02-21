import re
import sys
import os.path
from os import path

class Scanner:
    # --------compiled patterns---------
    open_comment = re.compile(r'/\*|//')
    close_comment = re.compile(r'\*/')
    special_sym = re.compile(r'\+|-|\*|/|<|>|;|,|\(|\)|\[|]|\{|}|=')
    compound_special_symbols = re.compile(r'>=|<=|!=|==')
    words = re.compile(r'[a-zA-Z]')
    Nums = re.compile(r'[0-9]')
    kw = re.compile(r'\belse\b|\bif\b|\breturn\b|\bvoid\b|\bwhile\b|\bint\b')

    tokens = []
    o = open('output.txt', 'w')

    def __init__(self, f):
        self.f = f
        self.line = self.f.readline()

    def error(self, text, i):
        error = text[i]
        i+=1
        self.tokens.append('ERROR')
        self.o.write('ERROR: ' + error + '\n')
        return i

    #process comments
    def comments(self, text, i, symbol):
        # global line
        self.line = text
        comment = ""
        if symbol == '//':
            self.line = self.f.readline()
            self.o.write('INPUT: ' + self.line)
            return 0
        else:
            while self.line and not self.line.isspace():
                x = re.search('\*/', self.line)
                if x:
                    return x.end()
                self.line = self.f.readline()
                self.o.write('INPUT: ' + self.line)

    #process special symbols
    def special_symbols(self, text, i):
        j = i+1
        while i < len(text) and re.match('[^\w\s]', text[i]):
            if j < len(text) and re.match('[^\w\s]', text[j]):
                if self.open_comment.match(text[i:j+1]):
                    return self.comments(text[i+2:len(text)], i, text[i:j+1])
                if self.compound_special_symbols.match(text[i:j+1]):
                    self.o.write(text[i:j + 1] + '\n')
                    self.tokens.append(text[i:j+1])
                    i += 2
                    j += 1
                elif self.special_sym.match(text[i]):
                    self.o.write(text[i] + '\n')
                    self.tokens.append(text[i])
                    i += 1
                    j += 1
                elif not self.special_sym.match(text[i]):
                    return self.error(text,i)
            else:
                if self.special_sym.match(text[i]):
                    self.o.write(text[i] + '\n')
                    self.tokens.append(text[i])
                elif not self.special_sym.match(text[i]):
                    return self.error(text,i)
                i += 1
        return i

    #process letters
    def letters(self, text, i):
        word = ""
        while i < len(text) and self.words.match(text[i]):
            word += text[i]
            if text[i] == '_':
                if self.words.match(word):
                    self.tokens.append('ID')
                    self.o.write(word + '\n')
                return self.error(text, i)
            i += 1
        if self.kw.match(word):
            self.tokens.append(word)
            self.o.write(word + '\n')
            return i
        else:
            self.o.write('ID: ' + word + '\n')
            self.tokens.append('ID')
        return i

    #process numbers
    def numbers(self, text, i):
        NUM = ""
        while i< len(text) and self.Nums.match(text[i]):
            NUM += text[i]
            i += 1
        self.o.write('NUM: ' + NUM + '\n')
        self.tokens.append('NUM')
        return i

    def run_scanner(self):
        while self.line:
            if self.line.isspace():
                self.line = self.f.readline()
                continue
            else: self.o.write('INPUT: ' + self.line)
            i = 0
            while i < len(self.line) and self.line[i] != '\n':
                if re.match('[a-zA-Z_]', self.line[i]):
                    i = self.letters(self.line, i)
                    continue
                elif self.Nums.match(self.line[i]):
                    i = self.numbers(self.line, i)
                    continue
                elif re.match(r'[^\w\s]', self.line[i]):
                    i = self.special_symbols(self.line, i)
                    continue
                else:
                    i += 1
            self.line = self.f.readline()
        self.tokens.append('$')

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
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens[self.count]
        print(tokens)

    def program(self):
        # print('in program')
        self.declaration_list()
        if self.tokens[self.count] == '$':
            return
        else:
            self.result = False

    def declaration_list(self):
        # print('in declaration_list')
        self.declaration()
        self.declaration_list_prime()

    def accept(self, token):
        self.count += 1
        self.current_token = self.tokens[self.count]

    def declaration_list_prime(self):
        # print('in declaration_list_prime')
        if self.current_token in ['int', 'void']:
            self.declaration()
            self.declaration_list_prime()

    def type_specifier(self):
        # print('in type_specifier')
        if self.current_token in ['int', 'void']:
            self.accept(self.current_token)
        else:
            self.result = False

    def declaration(self):
        # print('in declaration')
        self.type_specifier()
        if self.tokens[self.count] =='ID':
            self.accept('ID')
            self.declaration_prime()
        else:
            self.result = False


    def var_declaration(self):
        if self.tokens[self.count] == ';':
            self.accept(';')
            return
        elif self.tokens[self.count] == '[':
            self.accept('[')
            if self.tokens[self.count] == 'NUM':
                self.accept('NUM')
                if self.tokens[self.count] == ']':
                    self.accept(']')
                    if self.tokens[self.count] == ';':
                        self.accept(';')
                        return
        self.result = False

    def statement_list(self):
        # print('in statement_list')
        if self.current_token in self.statement_first:
            self.statement()
            self.statement_list()

    def local_declarations(self):
        if self.current_token in ['int', 'void']:
            self.accept(self.current_token)
            if self.tokens[self.count] == 'ID':
                self.accept('ID')
                self.var_declaration()
                self.local_declarations()


    def compound_stmt(self):
        if self.tokens[self.count] == '{':
            self.accept('{')
            self.local_declarations()
            self.statement_list()
            if self.tokens[self.count] == '}':
                self.accept('}')
            else:
                self.result = False
        else:
            self.result = False

    def declaration_prime(self):
        if self.tokens[self.count] in self.var_declaration_first:
            self.var_declaration()
        elif self.tokens[self.count] == '(':
            self.accept('(')
            self.params()
            if self.tokens[self.count] == ')':
                self.accept(')')
                self.compound_stmt()

    def param_prime(self):
        if self.tokens[self.count] == '[':
            self.accept('[')
            if self.tokens[self.count] == ']':
                self.accept(']')
            else:
                self.result = False

    def param(self):
        self.type_specifier()
        if self.tokens[self.count] == 'ID':
            self.accept('ID')
            self.param_prime()

    def param_list_prime(self):
        if self.tokens[self.count] == ',':
            self.accept(',')
            self.param_list()

    def param_list(self):
        self.param()
        self.param_list_prime()

    def params(self):
        if self.tokens[self.count] == 'void':
            self.accept('void')
            self.params_prime()
        elif self.tokens[self.count] == 'int':
            self.accept('int')
            if self.tokens[self.count] == 'ID':
                self.accept('ID')
                self.param_prime()
                self.param_list_prime()
        else:
            self.result = False

    def params_prime(self):
        if self.tokens[self.count] == 'ID':
            self.accept('ID')
            self.param_prime()
            self.param_list_prime()

    def statement(self):
        if self.tokens[self.count] in self.expression_stmt_first:
            self.expression_stmt()
        elif self.tokens[self.count] in self.compound_stmt_first:
            self.compound_stmt()
        elif self.tokens[self.count] == 'if':
            self.selection_stmt()
        elif self.tokens[self.count] == 'while':
            self.iteration_stmt()
        elif self.tokens[self.count] == 'return':
            self.return_stmt()
        else:
            self.result = False

    def selection_stmt(self):
        if self.tokens[self.count] == 'if':
            self.accept('if')
            if self.tokens[self.count] == '(':
                self.accept('(')
                self.expression()
                if self.tokens[self.count] == ')':
                    self.accept(')')
                    self.statement()
                    self.selection_stmt_prime()
                else:
                    self.result = False
            else:
                self.result = False

    def selection_stmt_prime(self):
        if self.tokens[self.count] == 'else':
            self.accept('else')
            self.statement()

    def iteration_stmt(self):
        if self.tokens[self.count] == 'while':
            self.accept('while')
            if self.tokens[self.count] == '(':
                self.accept('(')
                self.expression()
                if self.tokens[self.count] == ')':
                    self.accept(')')
                    self.statement()
                else:
                    self.result = False
            else:
                self.result = False

    def return_stmt(self):
        if self.tokens[self.count] == 'return':
            self.accept('return')
            self.return_stmt_prime()

    def return_stmt_prime(self):
        if self.tokens[self.count] == ';':
           self.accept(';')
        elif self.tokens[self.count] in self.expression_first:
            self.expression()
            if self.tokens[self.count] == ';':
                self.accept(';')
            else:
                self.result = False
        else:
            self.result = False


    def expression_stmt(self):
        if self.tokens[self.count] in self.expression_first:
            self.expression()
            if self.tokens[self.count] == ';':
                self.accept(';')
            else:
                self.result = False
        elif self.tokens[self.count] == ';':
            self.accept(';')
        else:
            self.result = False

    def expression(self):
        if self.tokens[self.count] == '(':
            self.accept('(')
            self.expression()
            if self.tokens[self.count] == ')':
                self.accept(')')
                self.term_prime()
                self.additive_expression_prime()
                self.simple_expression()
            else:
                self.result = False
        elif self.tokens[self.count] == 'ID':
            self.accept('ID')
            self.expression_prime()
        elif self.tokens[self.count] == 'NUM':
            self.accept('NUM')
            self.term_prime()
            self.additive_expression_prime()
            self.simple_expression()
        else:
            self.result = False

    def expression_prime(self):
        if self.current_token == '[':
            self.accept(self.current_token)
            self.expression()
            if self.tokens[self.count] == ']':
                self.accept(']')
                self.expression_double_prime()
            else:
                self.result = False
        elif self.tokens[self.count] == '(':
            self.accept('(')
            self.args()
            if self.tokens[self.count] == ')':
                self.accept(')')
                self.term_prime()
                self.additive_expression_prime()
                self.simple_expression()
            else:
                self.result = False
        elif self.tokens[self.count] in self.expression_double_prime_first:
            self.expression_double_prime()

    def expression_double_prime(self):
        if self.current_token == '=':
            self.accept(self.current_token)
            self.expression()
        else:
            self.term_prime()
            self.additive_expression_prime()
            self.simple_expression()

    def simple_expression(self):
        if self.current_token in ['<=', '<', '>', '>=', '==', '!=']:
            self.accept(self.current_token)
            self.additive_expression()

    def relop(self):
        r = ['<=', '<', '>', '>=', '==', '!=']
        if self.tokens[self.count] in r:
            self.accept(self.tokens[self.count])
        else:
            self.result = False

    def additive_expression(self):
        self.term()
        self.additive_expression_prime()

    def additive_expression_prime(self):
        if self.current_token in ['+', '-']:
            self.accept(self.current_token)
            self.term()
            self.additive_expression_prime()

    def term(self):
        self.factor()
        self.term_prime()

    def term_prime(self):
        if self.tokens[self.count] in ['*', '/']:
            self.accept(self.tokens[self.count])
            self.factor()
            self.term_prime()

    def factor(self):
        if self.current_token == '(':
            self.accept(self.current_token)
            self.expression()
            if self.current_token == ')':
                self.accept(self.current_token)
            else:
                self.result = False
        elif self.current_token == 'ID':
            self.accept(self.current_token)
            self.factor_prime()
        elif self.current_token == 'NUM':
            self.accept(self.current_token)
        else:
            self.result = False

    def factor_prime(self):
        if self.current_token == '[':
            self.accept(self.current_token)
            self.expression()
            if self.current_token == ']':
                self.accept(self.current_token)
            else:
                self.result = False
        elif self.current_token == '(':
            self.accept(self.current_token)
            self.args()
            if self.current_token == ')':
                self.accept(self.current_token)
            else:
                self.result = False

    def args(self):
        if self.current_token in self.expression_first:
            self.expression()
            self.arg_list()

    def arg_list(self):
        if self.current_token == ',':
            self.accept(self.current_token)
            self.expression()
            self.arg_list()

try:
    file = input()
    f = open(file, 'r')
    # file = sys.argv[1]
    scanner = Scanner(f)
    scanner.run_scanner()
    parse = Parser(scanner.tokens)
    parse.program()
    if parse.result == True:
        print('ACCEPT')
    else:
        print('REJECT')
except IOError:
    print('File not accessible')
finally:
    f.close

