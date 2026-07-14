#include <stdio.h>
void ft_swap(int *a, int *b);
int main(){int a=95, b=195; ft_swap(&a, &b); printf("%d %d", a, b); return 0;}