#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={74,-90,-76,36,63,-10,10,56,66,-31,-15,-31,-32,-75}; ft_rev_int_tab(tab, 14); for(int j=0; j<14; j++) printf("%d ", tab[j]); return 0;}