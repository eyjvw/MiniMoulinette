#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={92,5,97,-2,-40,69,12,85,63,-58}; ft_sort_int_tab(tab, 10); for(int j=0; j<10; j++) printf("%d ", tab[j]); return 0;}