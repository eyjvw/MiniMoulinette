#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-24,78,-1,-73,61,76,-9,24,-79,61,12,88,-52}; ft_sort_int_tab(tab, 13); for(int j=0; j<13; j++) printf("%d ", tab[j]); return 0;}