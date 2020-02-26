prj3: prj3.tab.o lex.yy.o
	cc -o p3 lex.yy.o prj3.tab.o

prj3.tab.o: prj3.tab.c
	cc -c prj3.tab.c

prj3.tab.c: prj3.y
	bison -d prj3.y

lex.yy.o: lex.yy.c prj3.tab.h
	cc -c lex.yy.c

lex.yy.c: prj3.l prj3.tab.c
	flex prj3.l

