#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-65,-91,-51,-94,84,51,-39,25,-1,-84,38,64,-22,27}; ft_rev_int_tab(tab, 14); for(int j=0; j<14; j++) printf("%d ", tab[j]); return 0;}