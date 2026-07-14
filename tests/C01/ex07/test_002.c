#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-86,67,-11}; ft_rev_int_tab(tab, 3); for(int j=0; j<3; j++) printf("%d ", tab[j]); return 0;}