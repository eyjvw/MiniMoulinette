#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-82,-82,46,86,-36}; ft_rev_int_tab(tab, 5); for(int j=0; j<5; j++) printf("%d ", tab[j]); return 0;}