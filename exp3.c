
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int isKeyword(char word[]) {
    char *keywords[] = {
        "int", "char", "float", "double", "void",
        "if", "else", "for", "while", "return",
        "main", "printf", "scanf"
    };
    int n = sizeof(keywords) / sizeof(keywords[0]);

    for (int i = 0; i < n; i++)
        if (strcmp(word, keywords[i]) == 0)
            return 1;

    return 0;
}

int main() {
    FILE *fp = fopen("flex_input.txt", "r");
    char ch, word[100];
    int i = 0, next;

    if (fp == NULL) {
        printf("Cannot open flex_input.txt");
        return 1;
    }

    while ((ch = fgetc(fp)) != EOF) {
        if (ch == '/') {
            next = fgetc(fp);

            if (next == '/') {
                while ((ch = fgetc(fp)) != EOF && ch != '\n');
                continue;
            }
            if (next == '*') {
                int prev = 0;
                while ((ch = fgetc(fp)) != EOF) {
                    if (prev == '*' && ch == '/') break;
                    prev = ch;
                }
                continue;
            }
            if (next != EOF) ungetc(next, fp);
            printf("/ is operator\n");
            continue;
        }

        if (isspace((unsigned char)ch))
            continue;

        if (isalnum((unsigned char)ch) || ch == '_') {
            i = 0;
            word[i++] = ch;

            while ((ch = fgetc(fp)) != EOF &&
                   (isalnum((unsigned char)ch) || ch == '_')) {
                if (i < 99) word[i++] = ch;
            }

            word[i] = '\0';

            if (ch != EOF) ungetc(ch, fp);

            if (isKeyword(word))
                printf("%s is keyword\n", word);
            else if (isdigit((unsigned char)word[0]))
                printf("%s is constant\n", word);
            else
                printf("%s is identifier\n", word);
        }
        else if (strchr("+-*%=<>", ch)) {
            printf("%c is operator\n", ch);
        }
    }

    fclose(fp);
    return 0;
}
