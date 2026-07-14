#include <stdio.h>
void ft_div_mod(int a, int b, int *div, int *mod);
int main(){int d=0, m=0; ft_div_mod(99, 9, &d, &m); printf("%d %d", d, m); return 0;}