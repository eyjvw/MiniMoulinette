#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-56,-51,-16,-14,72,22,21,-91,65,-66,23,-61,60,17,37,-15,18}; ft_sort_int_tab(tab, 17); for(int j=0; j<17; j++) printf("%d ", tab[j]); return 0;}