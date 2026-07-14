#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={57,47,14,-50,-48,74,-19,-24,45}; ft_sort_int_tab(tab, 9); for(int j=0; j<9; j++) printf("%d ", tab[j]); return 0;}