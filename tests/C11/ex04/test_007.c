#include <stdio.h>
int ft_is_sort(int *tab, int length, int (*f)(int, int));
static int cmp_asc(int a, int b){return a - b;}
int main(void){int tab[] = {-3, -1, 0, 7};printf("%d", ft_is_sort(tab, 4, cmp_asc));return 0;}
