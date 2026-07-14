#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={96,-24,-18,-6,-3,-83,94,9,40}; ft_rev_int_tab(tab, 9); for(int j=0; j<9; j++) printf("%d ", tab[j]); return 0;}