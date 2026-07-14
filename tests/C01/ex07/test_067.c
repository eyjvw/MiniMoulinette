#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={14,-6,-56,-34,100,79,-40,24}; ft_rev_int_tab(tab, 8); for(int j=0; j<8; j++) printf("%d ", tab[j]); return 0;}