#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={93,95,19,45,-67,-77,78,19,-76,16,-21,75,64,81,96,19}; ft_sort_int_tab(tab, 16); for(int j=0; j<16; j++) printf("%d ", tab[j]); return 0;}