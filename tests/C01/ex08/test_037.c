#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={21,-72,-11,22,18,-57,-28,96,-11,54,47,-68,30,-74,3,82,-73,-17}; ft_sort_int_tab(tab, 18); for(int j=0; j<18; j++) printf("%d ", tab[j]); return 0;}