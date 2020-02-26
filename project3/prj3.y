%{
#include <stdio.h>
#include <stdlib.h>
extern yylex();
extern yytext[];
extern FILE *yyin;
%}
%start start
%token RENAME AS LP RP WHERE LB RB bin_op comp attri RELATION VAL comma
%%
start         : expression                             {
                                                       printf("\nACCEPT\n");
                                                        };
expression    : one_relation_expression                 {
                                                        };
              | two_relation_expression                 {
                                                        };
one_relation_expression : renaming                      {
                                                        };
              | restriction                             {
                                                        };
              | projection                              {
                                                        };
renaming      : term RENAME attribute AS attribute      {
                                                        };
term          : relation                                {
                                                        };
              | LP expression RP                          {
                                                        };
restriction   : term WHERE comparison                   {
                                                        };
projection    : term                                    {
                                                        };
              | term LB attribute_commalist RB            {
                                                        };
attribute_commalist  : attribute                        {
                                                        };
              | attribute comma attribute_commalist         {
                                                        };
two_relation_expression : projection binary_operation expression {
                                                        };
binary_operation : bin_op                               {
                                                        };
comparison : attribute compare number                   {
                                                        };
compare : comp                                          {
                                                        };
number : val                                            {
                                                        };
        | val number                                    {
                                                        };
val : VAL                                               {
                                                        };
attribute : attri                                       {
                                                        };
relation : RELATION                                     {
                                                        };
%%
int main(int argc, char *argv[])
{
   yyin = fopen(argv[1], "r");
   if (!yyin)
   {
      printf("no file\n");
      exit(0);
   }
   yyparse();
}
yyerror()
{
   printf("\nREJECT\n");
//   printf("error from yyerror\n");
   exit(0);
}
yywrap()
{
   printf("in yywarp\n");
   exit(0);
}
