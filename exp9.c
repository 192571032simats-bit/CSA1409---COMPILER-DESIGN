
#include <stdio.h>

int main() {
    printf("Original Grammar:\n");
    printf("S -> (L) | a\n");
    printf("L -> L,S | S\n");

    printf("\nGrammar after eliminating left recursion:\n");
    printf("S -> (L) | a\n");
    printf("L -> SL'\n");
    printf("L' -> ,SL' | epsilon\n");

    return 0;
}
