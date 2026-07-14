#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={20,-41,-43,-64,57,-34,-7,0,-54,79,70,-16,-17,16,24,-93,-84}; ft_rev_int_tab(tab, 17); for(int j=0; j<17; j++) printf("%d ", tab[j]); return 0;}