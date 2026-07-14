#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-78,23,85,76,54,80,-27,9,55,-19,-34,34}; ft_sort_int_tab(tab, 12); for(int j=0; j<12; j++) printf("%d ", tab[j]); return 0;}