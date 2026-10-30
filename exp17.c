#include <stdio.h>
#include <ctype.h>

int main() {
    char str[1000];
    int characters = 0;
    int words = 0;
    int lines = 0;
    int in_word = 0;
    int i;

    printf("Enter text (press ~ to finish):\n");

    while ((str[0] = getchar()) != '~') {
        char ch = str[0];

        if (ch != '\n')
            characters++;

        if (ch == '\n')
            lines++;

        if (isspace((unsigned char)ch)) {
            in_word = 0;
        } else if (!in_word) {
            words++;
            in_word = 1;
        }
    }

    printf("Total number of words: %d\n", words);
    printf("Total number of lines: %d\n", lines);
    printf("Total number of characters: %d\n", characters);

    return 0;
}