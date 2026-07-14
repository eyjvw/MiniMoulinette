#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={23,87,34,-21,98}; ft_sort_int_tab(tab, 5); for(int j=0; j<5; j++) printf("%d ", tab[j]); return 0;}