#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-71,-97,59,43,31,-74,-48,38,-11,40,-19,-31}; ft_rev_int_tab(tab, 12); for(int j=0; j<12; j++) printf("%d ", tab[j]); return 0;}