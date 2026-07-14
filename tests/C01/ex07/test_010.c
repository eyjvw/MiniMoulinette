#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={34,-47,78,-47,56,-86,-73,46,86,61,35}; ft_rev_int_tab(tab, 11); for(int j=0; j<11; j++) printf("%d ", tab[j]); return 0;}