
#include <stdio.h>
#include <string.h>

int main() {
    char com[200];

    printf("Enter comment: ");
    fgets(com, sizeof(com), stdin);

    if (strncmp(com, "//", 2) == 0) {
        printf("It is a comment");
    }
    else if (strncmp(com, "/*", 2) == 0 &&
             strstr(com, "*/") != NULL) {
        printf("It is a comment");
    }
    else {
        printf("It is not a comment");
    }

    return 0;
}
