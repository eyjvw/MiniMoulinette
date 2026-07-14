#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-28,56,69,77,79,52,46}; ft_rev_int_tab(tab, 7); for(int j=0; j<7; j++) printf("%d ", tab[j]); return 0;}