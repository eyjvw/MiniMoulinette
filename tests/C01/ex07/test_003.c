#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-91,-63,-92,70}; ft_rev_int_tab(tab, 4); for(int j=0; j<4; j++) printf("%d ", tab[j]); return 0;}