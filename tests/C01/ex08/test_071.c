#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={18,2,21,-23,21,91,92,36,-41,-3,74,80}; ft_sort_int_tab(tab, 12); for(int j=0; j<12; j++) printf("%d ", tab[j]); return 0;}