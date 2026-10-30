#include <stdio.h>
#include <string.h>

int main() {
    char str[100];
    int i, b_found = 0, valid = 1;

    printf("The grammar is: S -> aS | Sb | ab\n");
    printf("Enter the string: ");
    scanf("%99s", str);

    if (str[0] != 'a') {
        valid = 0;
    } else {
        for (i = 1; str[i] != '\0'; i++) {
            if (str[i] == 'a' && b_found == 1) {
                valid = 0;
                break;
            } else if (str[i] == 'b') {
                b_found = 1;
            } else if (str[i] != 'a') {
                valid = 0;
                break;
            }
        }
    }

    if (valid && b_found)
        printf("String accepted\n");
    else
        printf("String not accepted\n");

    return 0;
}