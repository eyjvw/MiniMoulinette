#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={74,-23,2,-86,61,65,-77,-7,36,-13,-80}; ft_rev_int_tab(tab, 11); for(int j=0; j<11; j++) printf("%d ", tab[j]); return 0;}