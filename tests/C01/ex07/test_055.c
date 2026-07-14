#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={41,15,-2,-10,-43,-53,8,54,-99,47,27,87,-40,82,28,-32}; ft_rev_int_tab(tab, 16); for(int j=0; j<16; j++) printf("%d ", tab[j]); return 0;}