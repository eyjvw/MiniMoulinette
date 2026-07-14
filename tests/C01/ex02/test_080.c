#include <stdio.h>
void ft_swap(int *a, int *b);
int main(){int a=80, b=180; ft_swap(&a, &b); printf("%d %d", a, b); return 0;}