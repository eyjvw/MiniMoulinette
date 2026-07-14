#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-54,35,-92,-13,-79,-63,52,-61,26}; ft_sort_int_tab(tab, 9); for(int j=0; j<9; j++) printf("%d ", tab[j]); return 0;}