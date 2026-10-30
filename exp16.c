#include <stdio.h>
#include <string.h>

int main() {
    char expression[100];
    char result[20];
    char operand[20];
    char temp[20];
    int i, count = 1;

    printf("Enter expression (example: out=a+b+c-d): ");
    scanf("%99s", expression);

    char *equal = strchr(expression, '=');

    if (equal == NULL) {
        printf("Invalid expression\n");
        return 0;
    }

    *equal = '\0';
    strcpy(result, expression);

    char *token = strtok(equal + 1, "+-");

    if (token == NULL) {
        printf("Invalid expression\n");
        return 0;
    }

    strcpy(operand, token);

    char *operator_pos = equal + 1;
    while (*operator_pos != '\0') {
        char op = *operator_pos++;

        token = strtok(NULL, "+-");
        if (token == NULL)
            break;

        sprintf(temp, "t%d", count);

        printf("%s = %s %c %s\n",
               temp, operand, op, token);

        strcpy(operand, temp);
        count++;
    }

    printf("%s = %s\n", result, operand);

    return 0;
}