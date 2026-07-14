#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={6,5,-89,-15,-11,43,63,-46,-98,63,-49,76,-28,-35,-83}; ft_rev_int_tab(tab, 15); for(int j=0; j<15; j++) printf("%d ", tab[j]); return 0;}