#include <stdio.h>

int main() {
    printf("Grammar:\n");
    printf("E -> E+T | T\n");
    printf("T -> T*F | F\n");
    printf("F -> (E) | id\n");

    printf("\nLEADING sets:\n");

    printf("LEADING(E) = { +, *, (, i }\n");
    printf("LEADING(T) = { *, (, i }\n");
    printf("LEADING(F) = { (, i }\n");

    return 0;
}