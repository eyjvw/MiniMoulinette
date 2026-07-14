#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={69,-81,63,16,-30,96,9,77,70,97,97,-18,-35,-59,99,-82,-30,98,-85}; ft_sort_int_tab(tab, 19); for(int j=0; j<19; j++) printf("%d ", tab[j]); return 0;}