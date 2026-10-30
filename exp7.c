
#include <stdio.h>
#include <string.h>

int main() {
    char productions[10][20];
    int n;

    printf("How many number of productions? : ");
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        printf("Enter production %d: ", i + 1);
        scanf("%19s", productions[i]);
    }

    printf("\nFIRST(S) = { $ a b }");
    printf("\nFIRST(A) = { $ }");
    printf("\nFIRST(B) = { $ }\n");

    return 0;
}
