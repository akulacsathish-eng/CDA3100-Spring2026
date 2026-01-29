#include <stdio.h>
#include <stddef.h>

typedef unsigned char *pointer;

void show_bytes(pointer start, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%p\t0x%.2x\n", (void *)(start + i), start[i]);
    }
    printf("\n");
}

int main(void) {
    int a = 15213;

    printf("int a = %d\n", a);
    printf("Bytes of a in memory:\n");
    show_bytes((pointer)&a, sizeof(a));

    return 0;
}
