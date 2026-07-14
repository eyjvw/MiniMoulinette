#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-88,-73,6,-55,-59,72}; ft_rev_int_tab(tab, 6); for(int j=0; j<6; j++) printf("%d ", tab[j]); return 0;}