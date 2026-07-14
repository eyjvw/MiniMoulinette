#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-77,-45,-65,48,93,62,-100}; ft_sort_int_tab(tab, 7); for(int j=0; j<7; j++) printf("%d ", tab[j]); return 0;}