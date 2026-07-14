#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-10,-25,-26,-58,-91,77,52,91,-23,86,100,44,-34,-85,61,21,48,-57,46,-87}; ft_sort_int_tab(tab, 20); for(int j=0; j<20; j++) printf("%d ", tab[j]); return 0;}