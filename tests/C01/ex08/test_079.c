#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-3,-1,-15,-85,-34,-33,-55,12,-83,25,-49,56,0,-55,65,25,-73,-64,38,96}; ft_sort_int_tab(tab, 20); for(int j=0; j<20; j++) printf("%d ", tab[j]); return 0;}