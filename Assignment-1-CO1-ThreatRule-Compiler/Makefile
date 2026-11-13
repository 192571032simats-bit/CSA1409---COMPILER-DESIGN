FLEX ?= flex
CC ?= gcc
CFLAGS ?= -std=c99 -O2 -Wall -Wextra
SCANNER = LEX_Scanner/lex.yy.c
SPEC = LEX_Scanner/threatrule.l
PROGRAM = threatrule

all: $(PROGRAM)

$(SCANNER): $(SPEC)
	cd LEX_Scanner && $(FLEX) threatrule.l

$(PROGRAM): $(SCANNER)
	$(CC) $(CFLAGS) -o $(PROGRAM) $(SCANNER)

clean:
	rm -f $(SCANNER) $(PROGRAM) $(PROGRAM).exe

.PHONY: all clean
