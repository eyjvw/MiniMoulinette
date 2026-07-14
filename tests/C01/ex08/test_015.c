#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-22,-24,29,40,-18,96,-99,-71,75,-15,-13,1,85,45,57,-93}; ft_sort_int_tab(tab, 16); for(int j=0; j<16; j++) printf("%d ", tab[j]); return 0;}