#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={47,54,-24,-16,-78}; ft_sort_int_tab(tab, 5); for(int j=0; j<5; j++) printf("%d ", tab[j]); return 0;}