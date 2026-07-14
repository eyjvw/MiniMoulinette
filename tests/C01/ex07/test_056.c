#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={5,39,47,-7,-92,-91,45,23,80,-6,-72,48,23,76,-80,-64,86}; ft_rev_int_tab(tab, 17); for(int j=0; j<17; j++) printf("%d ", tab[j]); return 0;}