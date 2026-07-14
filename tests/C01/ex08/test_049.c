#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={73,-23,11,83,-12,-78,49,-98,56,30}; ft_sort_int_tab(tab, 10); for(int j=0; j<10; j++) printf("%d ", tab[j]); return 0;}