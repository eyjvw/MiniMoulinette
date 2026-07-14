#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-53,-63}; ft_rev_int_tab(tab, 2); for(int j=0; j<2; j++) printf("%d ", tab[j]); return 0;}