#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-69,81,-70,-78,54,-67,-4,68,95,65,44,-53,-72,78,-53,-36,-25,19}; ft_rev_int_tab(tab, 18); for(int j=0; j<18; j++) printf("%d ", tab[j]); return 0;}