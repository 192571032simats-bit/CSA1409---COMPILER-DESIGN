%option noyywrap
%{
#include "expr_parser.tab.h"
#include <stdlib.h>
%}
%%
[0-9]+  { yylval = atoi(yytext); return NUM; }
"+"    { return PLUS; }
"-"    { return MINUS; }
"*"    { return TIMES; }
"/"    { return DIV; }
"("    { return LP; }
")"    { return RP; }
[ 	
]+ ;
.       { return yytext[0]; }
%%
