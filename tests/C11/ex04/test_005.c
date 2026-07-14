#include <stdio.h>
int ft_is_sort(int *tab, int length, int (*f)(int, int));
static int cmp_asc(int a, int b){return a - b;}
int main(void){int tab[] = {5, 4, 6};printf("%d", ft_is_sort(tab, 3, cmp_asc));return 0;}
