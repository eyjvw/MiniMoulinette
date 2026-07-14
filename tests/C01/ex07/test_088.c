#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={25,22,11,3,86,99,-83,38,-43}; ft_rev_int_tab(tab, 9); for(int j=0; j<9; j++) printf("%d ", tab[j]); return 0;}