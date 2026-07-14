#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={47,59,-10,-67,57,44,27,33,86,61,27,26,-54}; ft_rev_int_tab(tab, 13); for(int j=0; j<13; j++) printf("%d ", tab[j]); return 0;}