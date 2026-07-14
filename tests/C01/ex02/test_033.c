#include <stdio.h>
void ft_swap(int *a, int *b);
int main(){int a=33, b=133; ft_swap(&a, &b); printf("%d %d", a, b); return 0;}