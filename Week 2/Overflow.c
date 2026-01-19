#include <stdio.h>
#include <stdint.h>

int main(void)
{
    uint8_t x = 250;
    uint8_t y = 10;
    uint8_t z = x + y;

    printf("x = %u\n", x);
    printf("y = %u\n", y);
    printf("x + y = %u\n", z);

    return 0;
}
