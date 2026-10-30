#include <stdio.h>
#include <string.h>

char input[100];
int i = 0;

int E();
int T();
int F();

int E() {
    if (!T())
        return 0;

    while (input[i] == '+' || input[i] == '-') {
        i++;
        if (!T())
            return 0;
    }
    return 1;
}

int T() {
    if (!F())
        return 0;

    while (input[i] == '*' || input[i] == '/') {
        i++;
        if (!F())
            return 0;
    }
    return 1;
}

int F() {
    if (input[i] == 'i') {
        i++;
        return 1;
    }

    if (input[i] == '(') {
        i++;
        if (E() && input[i] == ')') {
            i++;
            return 1;
        }
    }

    return 0;
}

int main() {
    printf("Enter the expression (use i for identifier): ");
    scanf("%99s", input);

    if (E() && input[i] == '\0')
        printf("Expression Accepted\n");
    else
        printf("Expression Rejected\n");

    return 0;
}