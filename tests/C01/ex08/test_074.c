#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-35,67,49,0,18,97,72,91,-39,87,72,50,97,-51,33}; ft_sort_int_tab(tab, 15); for(int j=0; j<15; j++) printf("%d ", tab[j]); return 0;}