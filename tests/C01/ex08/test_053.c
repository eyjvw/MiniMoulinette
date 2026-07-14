#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={6,-61,-27,71,-68,-66,-98,-82,65,-96,-64,84,24,68}; ft_sort_int_tab(tab, 14); for(int j=0; j<14; j++) printf("%d ", tab[j]); return 0;}