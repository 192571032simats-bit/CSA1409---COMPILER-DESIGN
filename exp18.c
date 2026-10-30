#include <stdio.h>

int main() {
    int n, i;
    char result, operand1, op, operand2;

    printf("Enter number of intermediate codes: ");
    scanf("%d", &n);

    for (i = 0; i < n; i++) {
        printf("Enter three address code (a=b+c): ");
        scanf(" %c=%c%c%c",
              &result, &operand1, &op, &operand2);

        printf("\nGenerated code:\n");
        printf("MOV %c, R%d\n", operand1, i);

        switch (op) {
            case '+':
                printf("ADD %c, R%d\n", operand2, i);
                break;

            case '-':
                printf("SUB %c, R%d\n", operand2, i);
                break;

            case '*':
                printf("MUL %c, R%d\n", operand2, i);
                break;

            case '/':
                printf("DIV %c, R%d\n", operand2, i);
                break;

            default:
                printf("Invalid operator\n");
                continue;
        }

        printf("MOV R%d, %c\n", i, result);
    }

    return 0;
}