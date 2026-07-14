#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={51,61,76,79,14,57,-9,-21,-15,-50,82,94,71,36,-80}; ft_rev_int_tab(tab, 15); for(int j=0; j<15; j++) printf("%d ", tab[j]); return 0;}