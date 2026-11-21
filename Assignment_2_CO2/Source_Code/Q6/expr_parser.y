%{
#include <stdio.h>
int yylex(void);
void yyerror(const char *s) {
    fprintf(stderr, "%s\n", s);
}
%}
%token NUM
%token PLUS MINUS TIMES DIV LP RP
%left PLUS MINUS
%left TIMES DIV
%%
expr:
    expr PLUS expr
  | expr MINUS expr
  | expr TIMES expr
  | expr DIV expr
  | LP expr RP
  | NUM
  ;
%%
int main(void) {
    yyparse();
    return 0;
}
