#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-14,73,76,-54,-20,40,-98,72,-98,-83,-97,5,-75,34,-74,75}; ft_rev_int_tab(tab, 16); for(int j=0; j<16; j++) printf("%d ", tab[j]); return 0;}