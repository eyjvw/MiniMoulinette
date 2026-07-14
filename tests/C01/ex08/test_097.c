#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-71,27,52,57,-44,-84,-49,9,-14,88,73,2,-17,-70,75,47,39,-65}; ft_sort_int_tab(tab, 18); for(int j=0; j<18; j++) printf("%d ", tab[j]); return 0;}