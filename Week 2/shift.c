#include <stdio.h>
#include <stdint.h>

int main(void)
{
    unsigned int x = 5;

    printf("x       = %u\n", x);
    printf("x << 1  = %u\n", x << 1);
    printf("x << 2  = %u\n", x << 2);
    printf("x >> 1  = %u\n", x >> 1);

    return 0;
}
