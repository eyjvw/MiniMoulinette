#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-72,54,-56,51,89,-62,68}; ft_rev_int_tab(tab, 7); for(int j=0; j<7; j++) printf("%d ", tab[j]); return 0;}