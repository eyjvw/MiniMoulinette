#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={100,5,90,-86,33,-24,44,85,73,-20,42,37,-96,-47,47,75,-16,-10}; ft_rev_int_tab(tab, 18); for(int j=0; j<18; j++) printf("%d ", tab[j]); return 0;}