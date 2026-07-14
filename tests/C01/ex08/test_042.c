#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={42,-76,13}; ft_sort_int_tab(tab, 3); for(int j=0; j<3; j++) printf("%d ", tab[j]); return 0;}