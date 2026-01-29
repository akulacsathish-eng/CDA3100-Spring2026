#include <stdio.h>

long sum_stride(const long *a, long n, long stride) {
    long acc = 0;

    for (long i = 0; i < n; i++) {
        acc += a[i * stride];
    }

    return acc;
}

int main(void) {
    long arr[16];

    for (int i = 0; i < 16; i++)
        arr[i] = i + 1;

    long s1 = sum_stride(arr, 8, 1);
    long s2 = sum_stride(arr, 8, 2);

    printf("sum_stride(arr,8,1) = %ld\n", s1);
    printf("sum_stride(arr,8,2) = %ld\n", s2);

    return 0;
}
