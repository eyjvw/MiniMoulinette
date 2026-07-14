#include <stdio.h>
int ft_ultimate_range(int **range, int min, int max);
int main(void){int *r = (void *)0; int n = ft_ultimate_range(&r, -10, -5);printf("n=%d:", n);if (r) for (int i = 0; i < n; i++) printf("%d ", r[i]);else printf("NULL");return 0;}
