#include <stdio.h>
#include <string.h>

char input[100];
char stack[100];
int top = -1;

void reduce() {
    if (top >= 0 &&
        (stack[top] == 'a' || stack[top] == 'b')) {
        stack[top] = 'E';
        stack[top + 1] = '\0';
        printf("Reduce: E -> a/b\n");
    }

    while (top >= 2) {
        if ((stack[top - 2] == 'E') &&
            (stack[top - 1] == '+' ||
             stack[top - 1] == '*' ||
             stack[top - 1] == '/') &&
            stack[top] == 'E') {

            char op = stack[top - 1];
            top -= 2;
            stack[top] = 'E';
            stack[top + 1] = '\0';

            printf("Reduce: E -> E %c E\n", op);
        } else {
            break;
        }
    }
}

int main() {
    int i;

    printf("SHIFT REDUCE PARSER\n");
    printf("Grammar: E -> E+E | E*E | E/E | a | b\n");
    printf("Enter input: ");
    scanf("%99s", input);

    printf("\nStack\tInput\tAction\n");

    for (i = 0; input[i] != '\0'; i++) {
        stack[++top] = input[i];
        stack[top + 1] = '\0';

        printf("%s\t%s\tShift\n", stack, input + i + 1);
        reduce();
    }

    if (top == 0 && stack[0] == 'E')
        printf("\nString Accepted\n");
    else
        printf("\nString Rejected\n");

    return 0;
}