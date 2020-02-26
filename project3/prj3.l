%{
#include "prj3.tab.h"
extern int yylval;
%}
Digit [0-9]
Delimiter [ \t]
WhiteSpace {Delimiter}+
Compare ["<>"|"<="|">="|"<"|">"|"="]
Attribute ["CNO"|"CITY"|"CNAME"|"SNO"|"PNO"|"TQTY"|"SNAME"|"QUOTA"|"PNAME"|"COST"|"AVQTY"|"S#"|"STATUS"|"P#"|"COLOR"|"WEIGHT"|"QTY"]
Relation ["S"|"P"|"SP"|"PRDCT"|"CUST"|"ORDERS"]
%%
{WhiteSpace}			;
"RENAME"			return(RENAME);
"AS"				return(AS);
"(" 				return(LP);
")"				return(RP);
"WHERE"				return(WHERE);
"["				return(LB);
"]"				return(RB);
"UNION"				return(bin_op);
"INTERSECTION"			return(bin_op);
"MINUS"				return(bin_op);
"TIMES"				return(bin_op);
"JOIN"				return(bin_op);
"DIVIDEBY"			return(bin_op);
","           return(comma);
{Compare}			return(comp);
{Digit}+			return(VAL);
{Attribute}			return(attri);
{Relation}			return(RELATION);
%%
