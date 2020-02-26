%{
#include "prj3.tab.h"
extern int yylval;
%}
Digit [0-9]
Delimiter [ \t]
WhiteSpace {Delimiter}+
%%
{WhiteSpace}			;
"RENAME"			   return(RENAME);
"AS"				     return(AS);
"(" 				     return(LP);
")"				       return(RP);
"WHERE"				   return(WHERE);
"["				       return(LB);
"]"				       return(RB);
"UNION"				   return(bin_op);
"INTERSECT"	     return(bin_op);
"MINUS"				   return(bin_op);
"TIMES"				   return(bin_op);
"JOIN"           return(bin_op);
"DIVIDEBY"			 return(bin_op);
","             return(comma);
"<>"            return (comp);
"<="            return(comp);
">="            return(comp);
"<"             return(comp);
">"             return(comp);
"="             return(comp);
"CNO"           return(attri);
"CITY"          return(attri);
"CNAME"         return(attri);
"SNO"           return(attri);
"PNO"           return(attri);
"TQTY"          return(attri);
"SNAME"         return(attri);
"QUOTA"         return(attri);
"PNAME"         return(attri);
"COST"          return(attri);
"AVQTY"         return(attri);
"S#"            return(attri);
"STATUS"         return(attri);
"P#"            return(attri);
"COLOR"         return(attri);
"WEIGHT"        return(attri);
"QTY"           return(attri);
"S"             return(RELATION);
"P"             return(RELATION);
"SP"            return(RELATION);
"PRDCT"         return(RELATION);
"CUST"          return(RELATION);
"ORDERS"        return(RELATION);
{Digit}+		  	return(VAL);
.               return(ERROR);
%%
