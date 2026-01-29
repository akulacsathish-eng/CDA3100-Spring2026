#include <stdio.h>

void swap_long(long *xp, long *yp) {
    long t0 = *xp;
    long t1 = *yp;
    *xp = t1;
    *yp = t0;
}

int main(void) {
    long a = 123;
    long b = 456;

    printf("Before swap: a=%ld b=%ld\n", a, b);
    swap_long(&a, &b);
    printf("After  swap: a=%ld b=%ld\n", a, b);

    return 0;
}
