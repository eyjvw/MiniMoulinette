#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={36,15,-96,-91,-14,-86,-14,84,-90,3,-70,-46,67,70,33}; ft_rev_int_tab(tab, 15); for(int j=0; j<15; j++) printf("%d ", tab[j]); return 0;}