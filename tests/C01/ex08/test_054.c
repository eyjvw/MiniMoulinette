#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={11,-66,-79,-65,64,6,16,78,54,8,59,-54,16,30,8}; ft_sort_int_tab(tab, 15); for(int j=0; j<15; j++) printf("%d ", tab[j]); return 0;}