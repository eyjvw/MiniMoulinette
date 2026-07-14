#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-84,-62,-29,-93,-14,-4,60,36,-58,46,55,-1,-53,52,-71,100,92,-22,80}; ft_sort_int_tab(tab, 19); for(int j=0; j<19; j++) printf("%d ", tab[j]); return 0;}