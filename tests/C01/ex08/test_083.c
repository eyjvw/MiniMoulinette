#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={83,-34,-74,-92}; ft_sort_int_tab(tab, 4); for(int j=0; j<4; j++) printf("%d ", tab[j]); return 0;}