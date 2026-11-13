%option noyywrap yylineno nodefault
%x COMMENT

%{
/* Standalone scanner: emit tokens/diagnostics and retain distinct identifiers. */
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned long token_count = 0;
static unsigned long error_count = 0;
static unsigned long newline_count = 0;
static int saw_input = 0;
static int last_input_was_newline = 0;
static int print_tokens = 1;
static int print_stats = 0;
static int legacy_mode = 0;
static int show_symbols = 0;
static int port_pending = 0;
static int comment_start_line = 1;
static char **symbol_names = NULL;
static size_t symbol_count = 0;
static size_t symbol_capacity = 0;

static void emit_token(const char *name);
static void report_error(const char *message);
static int valid_ipv4(const char *text);
static int valid_url(const char *text);
static int keyword_name(const char *text, const char **name);
static int equal_ignore_case(const char *a, const char *b);
static void emit_identifier(void);
static void emit_integer(void);
static void emit_extended(const char *name);
static void emit_operator(const char *name);
static void insert_symbol(const char *name);
static void print_symbols(void);
static void print_escaped_lexeme(void);
static void usage(const char *program);

#define YY_USER_ACTION do { \
    if (yyleng > 0) { \
        saw_input = 1; \
        last_input_was_newline = (yytext[yyleng - 1] == '\n'); \
        if (last_input_was_newline) ++newline_count; \
    } \
} while (0);
%}

 /* Reusable regular definitions; semantic actions check numeric ranges. */
DIGIT       [0-9]
ID_START    [A-Za-z_]
ID_CONT     [A-Za-z0-9_]
IDENT       {ID_START}{ID_CONT}*
IPV4        {DIGIT}+\.{DIGIT}+\.{DIGIT}+\.{DIGIT}+
INTEGER     {DIGIT}+
HEX         [A-Fa-f0-9]
HASH        ({HEX}{32}|{HEX}{40}|{HEX}{64})
CVE         [Cc][Vv][Ee]-{DIGIT}{4,}-[0-9]{1,}
URL         https?:\/\/[^ \t\r\n\";,' ]+
STRING      \"([^\"\\\r\n]|\\.)*\"
UNCLOSED    \"([^\"\\\r\n]|\\.)*

%%

 /* Separators and comments are discarded; Flex maintains yylineno. */
[ \t\r]+                         ;
\n                              ;
"//"[^\n]*                      ;
"#"[^\n]*                       ;
"/*"                            { comment_start_line = yylineno; BEGIN(COMMENT); }
<COMMENT>"*/"                   { BEGIN(INITIAL); }
<COMMENT>\n                     ;
<COMMENT>.                      ;
<COMMENT><<EOF>>                {
                                    char message[96];
                                    snprintf(message, sizeof(message),
                                             "unterminated block comment (started on line %d)",
                                             comment_start_line);
                                    report_error(message);
                                    BEGIN(INITIAL);
                                    return 0;
                                }

{STRING}                        { emit_token("STRING"); }
{UNCLOSED}                      { report_error("unterminated string literal"); }

"RULE"                          { emit_token("RULE"); }
"IF"                            { emit_token("IF"); }
"AND"                           { emit_token("AND"); }
"OR"                            { emit_token("OR"); }
"THEN"                          { emit_token("THEN"); }
"ALERT"                         { emit_token("ALERT"); }
"BLOCK"                         { emit_token("BLOCK"); }

{IPV4}                          {
                                    if (valid_ipv4(yytext)) {
                                        emit_token("IPV4");
                                    } else {
                                        report_error("IPv4 octets must each be in the range 0..255");
                                    }
                                }
 /* Day-4 live-feed additions; their patterns outmatch identifier fragments. */
{CVE}                           {
                                    if (legacy_mode) {
                                        report_error("CVE identifiers are unsupported by the original scanner");
                                    } else {
                                        emit_extended("CVE");
                                    }
                                }
{HASH}                          {
                                    if (legacy_mode) {
                                        report_error("file hashes are unsupported by the original scanner");
                                    } else {
                                        emit_extended("HASH");
                                    }
                                }
{URL}                           {
                                    if (legacy_mode) {
                                        report_error("URLs are unsupported by the original scanner");
                                    } else if (valid_url(yytext)) {
                                        emit_extended("URL");
                                    } else {
                                        report_error("URL is outside the documented http(s) syntax");
                                    }
                                }

{IDENT}                         {
                                    if (port_pending) port_pending = 0;
                                    emit_identifier();
                                }
{INTEGER}                       { emit_integer(); }

"=="                            { emit_operator("EQ"); }
"!="                            { emit_operator("NE"); }
"<="                            { emit_operator("LE"); }
">="                            { emit_operator("GE"); }
"<"                             { emit_operator("LT"); }
">"                             { emit_operator("GT"); }
"="                             { emit_operator("ASSIGN"); }
";"                             { emit_token("SEMICOLON"); }
"("                             { emit_token("LPAREN"); }
")"                             { emit_token("RPAREN"); }
"{"                             { emit_token("LBRACE"); }
"}"                             { emit_token("RBRACE"); }

.                               { report_error("invalid character"); }

%%

static int equal_ignore_case(const char *a, const char *b)
{
    while (*a && *b) {
        if (toupper((unsigned char)*a) != toupper((unsigned char)*b)) return 0;
        ++a;
        ++b;
    }
    return *a == '\0' && *b == '\0';
}

static int keyword_name(const char *text, const char **name)
{
    static const char *const words[][2] = {
        {"RULE", "RULE"}, {"IF", "IF"}, {"AND", "AND"}, {"OR", "OR"},
        {"THEN", "THEN"}, {"ALERT", "ALERT"}, {"BLOCK", "BLOCK"}
    };
    size_t i;
    for (i = 0; i < sizeof(words) / sizeof(words[0]); ++i) {
        if (equal_ignore_case(text, words[i][0])) {
            *name = words[i][1];
            return 1;
        }
    }
    return 0;
}

static int valid_ipv4(const char *text)
{
    int octet, digits, value;
    const char *p = text;
    int part;
    for (part = 0; part < 4; ++part) {
        value = 0;
        digits = 0;
        while (*p >= '0' && *p <= '9') {
            value = value * 10 + (*p++ - '0');
            if (++digits > 3 || value > 255) return 0;
        }
        if (digits == 0) return 0;
        octet = value;
        if (octet < 0 || octet > 255) return 0;
        if (part < 3) {
            if (*p++ != '.') return 0;
        }
    }
    return *p == '\0';
}

static int valid_url(const char *text)
{
    const char *host, *end, *p;
    size_t label_length = 0;
    if (strncmp(text, "http://", 7) == 0) host = text + 7;
    else if (strncmp(text, "https://", 8) == 0) host = text + 8;
    else return 0;
    end = host;
    while (*end && *end != '/' && *end != '?' && *end != '#') ++end;
    if (end == host || (size_t)(end - host) > 253) return 0;
    for (p = host; p < end; ++p) {
        if (*p == '.') {
            if (label_length == 0 || p[-1] == '-') return 0;
            label_length = 0;
        } else {
            if (!(isalnum((unsigned char)*p) || *p == '-')) return 0;
            if (label_length == 0 && *p == '-') return 0;
            if (++label_length > 63) return 0;
        }
    }
    if (label_length == 0 || end[-1] == '-') return 0;
    for (p = end; *p; ++p) {
        if (isspace((unsigned char)*p) || *p == '"' || *p == '\'' ||
            *p == ';' || *p == ',') return 0;
    }
    return 1;
}

static void print_escaped_lexeme(void)
{
    int i;
    for (i = 0; i < yyleng; ++i) {
        unsigned char c = (unsigned char)yytext[i];
        if (c == '\\' || c == '"') putchar('\\');
        if (c == '\n') fputs("\\n", stdout);
        else if (c == '\r') fputs("\\r", stdout);
        else if (c == '\t') fputs("\\t", stdout);
        else putchar(c);
    }
}

static void emit_token(const char *name)
{
    const char *keyword;
    ++token_count;
    if (equal_ignore_case(name, "IDENTIFIER") &&
        keyword_name(yytext, &keyword)) name = keyword;
    if (print_tokens) {
        printf("%d:%s:", yylineno, name);
        print_escaped_lexeme();
        putchar('\n');
    }
}

static void emit_identifier(void)
{
    const char *keyword;
    if (equal_ignore_case(yytext, "port")) {
        port_pending = 1;
    } else if (keyword_name(yytext, &keyword)) {
        emit_token(keyword);
        return;
    }
    insert_symbol(yytext);
    emit_token("IDENTIFIER");
}

static void emit_integer(void)
{
    char *end = NULL;
    unsigned long value;
    errno = 0;
    value = strtoul(yytext, &end, 10);
    /* A port's range depends on its field context, unlike general integers. */
    if (port_pending) {
        port_pending = 0;
        if (errno == ERANGE || end == yytext || *end != '\0' || value > 65535UL) {
            report_error("port value must be in the range 0..65535");
            return;
        }
        emit_token("PORT");
        return;
    }
    emit_token("INTEGER");
}

static void emit_extended(const char *name)
{
    emit_token(name);
}

static void emit_operator(const char *name)
{
    emit_token(name);
}

static void insert_symbol(const char *name)
{
    size_t i;
    char *copy;
    for (i = 0; i < symbol_count; ++i) {
        if (strcmp(symbol_names[i], name) == 0) return;
    }
    if (symbol_count == symbol_capacity) {
        size_t next_capacity = symbol_capacity == 0 ? 32 : symbol_capacity * 2;
        char **next = (char **)realloc(symbol_names, next_capacity * sizeof(*next));
        if (next == NULL) {
            fprintf(stderr, "fatal: unable to grow symbol table\n");
            exit(2);
        }
        symbol_names = next;
        symbol_capacity = next_capacity;
    }
    copy = (char *)malloc((size_t)yyleng + 1);
    if (copy == NULL) {
        fprintf(stderr, "fatal: unable to store identifier in symbol table\n");
        exit(2);
    }
    memcpy(copy, name, (size_t)yyleng);
    copy[yyleng] = '\0';
    symbol_names[symbol_count++] = copy;
}

static void print_symbols(void)
{
    size_t i;
    for (i = 0; i < symbol_count; ++i) {
        printf("SYMBOL[%lu]=%s\n", (unsigned long)i, symbol_names[i]);
    }
}

static void report_error(const char *message)
{
    ++error_count;
    fprintf(stderr, "line %d: lexical error: %s: ", yylineno, message);
    {
        int i;
        for (i = 0; i < yyleng; ++i) {
            unsigned char c = (unsigned char)yytext[i];
            if (c == '\n') fputs("\\n", stderr);
            else if (c == '\r') fputs("\\r", stderr);
            else if (c == '\t') fputs("\\t", stderr);
            else fputc(c, stderr);
        }
    }
    fputc('\n', stderr);
}

static void usage(const char *program)
{
    fprintf(stderr, "Usage: %s [--quiet] [--stats] [--symbols] [--legacy] [input-file]\n", program);
}

int main(int argc, char **argv)
{
    int i;
    for (i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--quiet") == 0) print_tokens = 0;
        else if (strcmp(argv[i], "--stats") == 0) print_stats = 1;
        else if (strcmp(argv[i], "--symbols") == 0) show_symbols = 1;
        else if (strcmp(argv[i], "--legacy") == 0) legacy_mode = 1;
        else if (argv[i][0] == '-') {
            usage(argv[0]);
            return 2;
        } else if (yyin == NULL) {
            yyin = fopen(argv[i], "rb");
            if (!yyin) {
                perror(argv[i]);
                return 2;
            }
        } else {
            usage(argv[0]);
            if (yyin != stdin) fclose(yyin);
            return 2;
        }
    }
    if (yyin == NULL) yyin = stdin;
    yylex();
    if (show_symbols) print_symbols();
    if (print_stats) {
        printf("TOKENS=%lu ERRORS=%lu LINES=%d\n",
               token_count, error_count,
               (int)(newline_count + (saw_input && !last_input_was_newline ? 1UL : 0UL)));
    }
    for (i = 0; i < (int)symbol_count; ++i) free(symbol_names[i]);
    free(symbol_names);
    if (yyin != stdin) fclose(yyin);
    return error_count == 0 ? 0 : 1;
}
