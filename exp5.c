
#include <stdio.h>

int main() {
    char str[1000];
    int spaces = 0, newlines = 0;

    printf("Enter text (press ~ to finish):\n");

    int i = 0;
    char ch;

    while ((ch = getchar()) != '~' && ch != EOF &&
           i < 999) {
        str[i++] = ch;
    }
    str[i] = '\0';

    for (int j = 0; str[j] != '\0'; j++) {
        if (str[j] == ' ')
            spaces++;
        else if (str[j] == '\n')
            newlines++;
    }

    printf("Total number of whitespaces: %d\n", spaces);
    printf("Total number of newline characters: %d\n", newlines);

    return 0;
}
