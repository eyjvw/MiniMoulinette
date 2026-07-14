#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={3,-68,-25,-85,-6,40,-87,-100,80,43,-9}; ft_rev_int_tab(tab, 11); for(int j=0; j<11; j++) printf("%d ", tab[j]); return 0;}