
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main() {
    char str[200];
    int i = 0;

    printf("Enter the string: ");
    fgets(str, sizeof(str), stdin);

    printf("Identifiers: ");
    while (str[i] != '\0') {
        if (isalpha((unsigned char)str[i]) || str[i] == '_') {
            while (isalnum((unsigned char)str[i]) || str[i] == '_')
                putchar(str[i++]);
            printf(" ");
        } else {
            i++;
        }
    }

    i = 0;
    printf("\nConstants: ");
    while (str[i] != '\0') {
        if (isdigit((unsigned char)str[i])) {
            while (isdigit((unsigned char)str[i]))
                putchar(str[i++]);
            printf(" ");
        } else {
            i++;
        }
    }

    printf("\nOperators: ");
    for (i = 0; str[i] != '\0'; i++) {
        if (strchr("+-*/%=<>", str[i]))
            printf("%c ", str[i]);
    }

    return 0;
}
