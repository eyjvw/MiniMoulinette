#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={93,-63,69,-62,15,36,-26,-1}; ft_rev_int_tab(tab, 8); for(int j=0; j<8; j++) printf("%d ", tab[j]); return 0;}