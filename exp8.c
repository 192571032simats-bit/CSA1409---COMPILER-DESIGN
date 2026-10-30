
#include <stdio.h>

int main() {
    char ch, choice;

    printf("Grammar:\n");
    printf("S -> AaAb / BbBa\n");
    printf("A -> $\n");
    printf("B -> $\n");

    do {
        printf("\nEnter production value to find FOLLOW: ");
        scanf(" %c", &ch);

        if (ch == 'S')
            printf("FOLLOW(S) = { $ }");
        else if (ch == 'A')
            printf("FOLLOW(A) = { a b }");
        else if (ch == 'B')
            printf("FOLLOW(B) = { b a }");
        else
            printf("Invalid non-terminal");

        printf("\nTo continue, press Y: ");
        scanf(" %c", &choice);

    } while (choice == 'y' || choice == 'Y');

    return 0;
}
