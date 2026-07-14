#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={17,94,96,-26,65,-49,-55,41,-90,-2,69,-52}; ft_rev_int_tab(tab, 12); for(int j=0; j<12; j++) printf("%d ", tab[j]); return 0;}