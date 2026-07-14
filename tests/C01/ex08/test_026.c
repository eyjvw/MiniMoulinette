#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-67,-48,85,-91,17,-1,82}; ft_sort_int_tab(tab, 7); for(int j=0; j<7; j++) printf("%d ", tab[j]); return 0;}