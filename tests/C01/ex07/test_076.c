#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={14,-11,-44,85,-28,-36,-51,-92,-94,58,-77,-86,52,68,-45,53,63}; ft_rev_int_tab(tab, 17); for(int j=0; j<17; j++) printf("%d ", tab[j]); return 0;}