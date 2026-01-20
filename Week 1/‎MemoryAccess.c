
#include <stdio.h>
#include <time.h>
#define N 2000
int A[N][N];
int main(void)
{
    int i, j;
    clock_t start, end;
    double time_taken;
    /* Initialize array */
    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++)
            A[i][j] = 1;
    /* Row-major access */
    start = clock();
    long long sum1 = 0;
    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++)
            sum1 += A[i][j];
    end = clock();
    time_taken = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Row-wise sum time: %.4f seconds (sum = %lld)\n", time_taken, sum1);
    /* Column-major access */
    start = clock();
    long long sum2 = 0;
    for (j = 0; j < N; j++)
        for (i = 0; i < N; i++)
            sum2 += A[i][j];
    end = clock();
    time_taken = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Column-wise sum time: %.4f seconds (sum = %lld)\n", time_taken, sum2);
    return 0;
}
