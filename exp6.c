
#include <stdio.h>
#include <ctype.h>

int main() {
    char a[100];
    int i, valid = 1;

    printf("Enter an identifier: ");
    scanf("%99s", a);

    if (!isalpha((unsigned char)a[0]) && a[0] != '_')
        valid = 0;

    for (i = 1; a[i] != '\0'; i++) {
        if (!isalnum((unsigned char)a[i]) && a[i] != '_') {
            valid = 0;
            break;
        }
    }

    if (valid)
        printf("Valid identifier");
    else
        printf("Not a valid identifier");

    return 0;
}
