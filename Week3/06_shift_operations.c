#include <stdio.h>
#include <stdint.h>

int main(void) {
    int64_t s = -16;
    uint64_t u = 16;

    printf("Signed value s = %lld\n", (long long)s);
    printf("Unsigned value u = %llu\n\n", (unsigned long long)u);

    printf("s >> 2 = %lld   (arithmetic right shift)\n", (long long)(s >> 2));
    printf("u >> 2 = %llu   (logical right shift)\n", (unsigned long long)(u >> 2));
    printf("u << 3 = %llu   (left shift)\n", (unsigned long long)(u << 3));

    return 0;
}
