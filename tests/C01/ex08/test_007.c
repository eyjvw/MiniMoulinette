#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={43,-55,16,91,48,-8,-91,-77}; ft_sort_int_tab(tab, 8); for(int j=0; j<8; j++) printf("%d ", tab[j]); return 0;}