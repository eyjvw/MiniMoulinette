#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-1,21,-33,-63,35,11,-97,-27,14,-3,73,-20,35}; ft_sort_int_tab(tab, 13); for(int j=0; j<13; j++) printf("%d ", tab[j]); return 0;}