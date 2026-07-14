#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={98,14,-96,27,-62,67}; ft_sort_int_tab(tab, 6); for(int j=0; j<6; j++) printf("%d ", tab[j]); return 0;}