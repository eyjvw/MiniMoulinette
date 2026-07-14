#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-67,-93,20,72,-88,-73,-2,-87,-78,9,0,-55,80,52}; ft_sort_int_tab(tab, 14); for(int j=0; j<14; j++) printf("%d ", tab[j]); return 0;}