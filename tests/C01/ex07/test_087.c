#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={79,-16,0,47,-100,31,81,97}; ft_rev_int_tab(tab, 8); for(int j=0; j<8; j++) printf("%d ", tab[j]); return 0;}