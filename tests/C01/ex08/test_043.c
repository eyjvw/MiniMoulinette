#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-55,-22,3,-83}; ft_sort_int_tab(tab, 4); for(int j=0; j<4; j++) printf("%d ", tab[j]); return 0;}