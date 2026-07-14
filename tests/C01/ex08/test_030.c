#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-30,36,-19,97,12,71,-70,-31,-62,-60,-30}; ft_sort_int_tab(tab, 11); for(int j=0; j<11; j++) printf("%d ", tab[j]); return 0;}