#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-15,19,-89,-74,33,96,68,90,-21}; ft_sort_int_tab(tab, 9); for(int j=0; j<9; j++) printf("%d ", tab[j]); return 0;}