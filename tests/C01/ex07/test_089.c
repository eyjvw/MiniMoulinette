#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-100,-2,76,99,23,-69,45,37,-9,-15}; ft_rev_int_tab(tab, 10); for(int j=0; j<10; j++) printf("%d ", tab[j]); return 0;}