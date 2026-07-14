#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={3,-3,11,39,-46,69,-56,21,-65,-52,42,-2,-8}; ft_sort_int_tab(tab, 13); for(int j=0; j<13; j++) printf("%d ", tab[j]); return 0;}