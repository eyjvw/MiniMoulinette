#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={87,34,92,99,-29,19,32,-80,33,56,-78,-38,20,61,89,69,71,-81}; ft_sort_int_tab(tab, 18); for(int j=0; j<18; j++) printf("%d ", tab[j]); return 0;}