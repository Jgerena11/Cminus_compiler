import re
import sys

file = sys.argv[1]
f = open(file, "r")
line = f.readline()
o = open('output.txt', 'w')

# --------compiled patterns---------
open_comment = re.compile(r'/\*|//')
close_comment = re.compile(r'\*/')
special_sym = re.compile(r'\+|-|\*|/|<|>|;|,|\(|\)|\[|]|\{|}|=')
compound_special_symbols = re.compile(r'>=|<=|!=|==')
words = re.compile(r'[a-zA-Z]')
Nums = re.compile(r'[0-9]')
kw = re.compile(r'\belse\b|\bif\b|\breturn\b|\bvoid\b|\bwhile\b|\bint\b')

# ---------functions------------
def error(text, i):
    error = text[i]
    i+=1
    o.write('ERROR: ' + error + '\n')
    return i

#process comments
def comments(text, i, symbol):
    global line
    line = text
    comment = ""
    if symbol == '//':
        line = f.readline()
        o.write('INPUT: ' + line)
        return 0
    else:
        while line and not line.isspace():
            x = re.search('\*/', line)
            if x:
                return x.end()
            line = f.readline()
            o.write('INPUT: ' + line)

#process special symbols
def special_symbols(text, i):
    j = i+1
    while i < len(text) and re.match('[^\w\s]', text[i]):

        if j < len(text) and re.match('[^\w\s]', text[j]):
            if open_comment.match(text[i:j+1]):
                return comments(text[i+2:len(text)], i, text[i:j+1])
            if compound_special_symbols.match(text[i:j+1]):
                o.write(text[i:j+1]+'\n')
                i += 2
                j += 1
            elif special_sym.match(text[i]):
                o.write(text[i]+'\n')
                i += 1
                j += 1
            elif not special_sym.match(text[i]):
                return error(text,i)
        else:
            if special_sym.match(text[i]):
                o.write(text[i]+'\n')
            elif not special_sym.match(text[i]):
                return error(text,i)
            i += 1
    return i

#process letters
def letters(text, i):
    word = ""
    while i < len(text) and words.match(text[i]):
        word += text[i]
        i += 1
    if text[i] == '_':
        if words.match(word): o.write('ID: ' + word + '\n')
        return error(text, i)
    if kw.match(word):
        o.write(word + '\n')
        return i
    else:
        o.write('ID: ' + word + '\n')
    return i

#process numbers
def numbers(text, i):
    NUM = ""
    while i< len(text) and Nums.match(text[i]):
        NUM += text[i]
        i += 1
    o.write('NUM: ' + NUM + '\n')
    return i

while line:
    if line.isspace():
        line = f.readline()
        continue
    else:
        o.write('INPUT: ' + line)
    i = 0
    while i < len(line) and line[i] != '\n':
        if re.match('[a-zA-Z_]', line[i]):
            i = letters(line, i)
            continue
        elif Nums.match(line[i]):
            i = numbers(line, i)
            continue
        elif re.match(r'[^\w\s]', line[i]):
            i = special_symbols(line, i)
            continue
        else:
            i += 1
    line = f.readline()
f.close()
o.close()