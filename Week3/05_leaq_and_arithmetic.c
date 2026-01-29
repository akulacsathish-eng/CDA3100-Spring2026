#include <stdio.h>

long mul12(long x) {
    return x * 12;
}

long arith(long x, long y, long z) {
    long t1 = x + y;
    long t2 = z + t1;
    long t3 = x + 4;
    long t4 = y * 48;
    long t5 = t3 + t4;
    return t2 * t5;
}

int main(void) {
    printf("mul12(7) = %ld\n", mul12(7));
    printf("arith(2,3,4) = %ld\n", arith(2,3,4));

    return 0;
}
