#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={17,73,37,-62,89,48,-41,-82,-91,88,-64,25,67,-96,20,58}; ft_sort_int_tab(tab, 16); for(int j=0; j<16; j++) printf("%d ", tab[j]); return 0;}