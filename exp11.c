#include <stdio.h>
#include <string.h>

struct Symbol {
    char label[20];
    int address;
};

struct Symbol table[50];
int count = 0;

int search(char label[]) {
    for (int i = 0; i < count; i++) {
        if (strcmp(table[i].label, label) == 0)
            return i;
    }
    return -1;
}

int main() {
    int choice, address, pos;
    char label[20];

    while (1) {
        printf("\n1.Insert\n2.Display\n3.Search\n4.Modify\n5.Exit\n");
        printf("Enter choice: ");
        scanf("%d", &choice);

        switch (choice) {
        case 1:
            if (count >= 50) {
                printf("Symbol table is full\n");
                break;
            }
            printf("Enter label: ");
            scanf("%19s", label);

            if (search(label) != -1) {
                printf("Duplicate symbol\n");
            } else {
                printf("Enter address: ");
                scanf("%d", &address);
                strcpy(table[count].label, label);
                table[count].address = address;
                count++;
                printf("Symbol inserted\n");
            }
            break;

        case 2:
            printf("\nLabel\tAddress\n");
            for (int i = 0; i < count; i++)
                printf("%s\t%d\n", table[i].label,
                       table[i].address);
            break;

        case 3:
            printf("Enter label: ");
            scanf("%19s", label);
            pos = search(label);
            if (pos != -1)
                printf("Label is found\n");
            else
                printf("Label is not found\n");
            break;

        case 4:
            printf("Enter label: ");
            scanf("%19s", label);
            pos = search(label);
            if (pos == -1) {
                printf("No such symbol\n");
            } else {
                printf("Enter new address: ");
                scanf("%d", &table[pos].address);
                printf("Address modified\n");
            }
            break;

        case 5:
            return 0;

        default:
            printf("Invalid choice\n");
        }
    }
}