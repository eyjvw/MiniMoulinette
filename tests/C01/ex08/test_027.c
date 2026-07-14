#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={33,-71,-99,-21,-89,75,52,-78}; ft_sort_int_tab(tab, 8); for(int j=0; j<8; j++) printf("%d ", tab[j]); return 0;}