#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-72,-28,-93,-40,10,79,51,0,60,-19,82,-3}; ft_sort_int_tab(tab, 12); for(int j=0; j<12; j++) printf("%d ", tab[j]); return 0;}