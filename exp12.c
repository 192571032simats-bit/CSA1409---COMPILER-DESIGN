#include <stdio.h>
#include <ctype.h>

char input[100];
int i = 0;

int E();
int EP();
int T();
int TP();
int F();

int E() {
    return T() && EP();
}

int EP() {
    if (input[i] == '+') {
        i++;
        return T() && EP();
    }
    return 1;
}

int T() {
    return F() && TP();
}

int TP() {
    if (input[i] == '*') {
        i++;
        return F() && TP();
    }
    return 1;
}

int F() {
    if (input[i] == '(') {
        i++;
        if (E() && input[i] == ')') {
            i++;
            return 1;
        }
        return 0;
    }

    if (isalpha((unsigned char)input[i])) {
        i++;
        return 1;
    }

    return 0;
}

int main() {
    printf("Enter the string: ");
    scanf("%99s", input);

    if (E() && input[i] == '\0')
        printf("String is accepted\n");
    else
        printf("String is not accepted\n");

    return 0;
}