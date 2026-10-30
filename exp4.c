
#include <stdio.h>
#include <string.h>

int main() {
    char s[10];

    printf("Enter any operator: ");
    scanf("%9s", s);

    if (strcmp(s, "<=") == 0)
        printf("Less than or equal");
    else if (strcmp(s, ">=") == 0)
        printf("Greater than or equal");
    else if (strcmp(s, "==") == 0)
        printf("Equal");
    else if (strcmp(s, "!=") == 0)
        printf("Not Equal");
    else if (strcmp(s, "&&") == 0)
        printf("Logical AND");
    else if (strcmp(s, "||") == 0)
        printf("Logical OR");
    else if (strcmp(s, "=") == 0)
        printf("Assignment");
    else if (strcmp(s, "<") == 0)
        printf("Less than");
    else if (strcmp(s, ">") == 0)
        printf("Greater than");
    else if (strcmp(s, "+") == 0)
        printf("Addition");
    else if (strcmp(s, "-") == 0)
        printf("Subtraction");
    else if (strcmp(s, "*") == 0)
        printf("Multiplication");
    else if (strcmp(s, "/") == 0)
        printf("Division");
    else if (strcmp(s, "%") == 0)
        printf("Modulus");
    else if (strcmp(s, "!") == 0)
        printf("Logical NOT");
    else
        printf("Not an operator");

    return 0;
}
