#include <stdio.h>

long plus(long x, long y) {
    return x + y;
}

void sumstore(long x, long y, long *dest) {
    long t = plus(x, y);
    *dest = t;
}

int main(void) {
    long out = 0;

    sumstore(10, 20, &out);

    printf("Result stored through pointer = %ld\n", out);

    return 0;
}
