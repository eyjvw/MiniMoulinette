#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-95,47,94,-21,63,-47,-18,-49,-51,-27}; ft_rev_int_tab(tab, 10); for(int j=0; j<10; j++) printf("%d ", tab[j]); return 0;}