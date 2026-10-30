
#include <stdio.h>
#include <string.h>

int main() {
    char production[100];
    char *arrow, *first, *second;
    int i = 0;

    printf("Enter Production: ");
    scanf("%99s", production);

    arrow = strstr(production, "->");

    if (arrow == NULL) {
        printf("Invalid production");
        return 0;
    }

    *arrow = '\0';
    first = arrow + 2;

    second = strchr(first, '|');

    if (second == NULL) {
        printf("No left factoring required");
        return 0;
    }

    *second = '\0';
    second++;

    while (first[i] && second[i] && first[i] == second[i])
        i++;

    if (i == 0) {
        printf("No common prefix found");
        return 0;
    }

    printf("\n%s -> ", production);
    for (int j = 0; j < i; j++)
        putchar(first[j]);

    printf("X\nX -> ");

    printf("%s | %s\n", first + i, second + i);

    return 0;
}
