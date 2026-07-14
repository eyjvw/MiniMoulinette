#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-64,80,-28,46,-38,-57,-82,-21,56,-14,38,13,-88}; ft_rev_int_tab(tab, 13); for(int j=0; j<13; j++) printf("%d ", tab[j]); return 0;}