#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={42,66,-82,-23,36,18,2,51,5,-39,58,-38,40,-60,23,-2,-84,-13,-47}; ft_sort_int_tab(tab, 19); for(int j=0; j<19; j++) printf("%d ", tab[j]); return 0;}