#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-20,81,-92,-31,5,-78,27,-40,-5,15,-23,-45,34,-23,-56,-72,-5,100,-91,99}; ft_rev_int_tab(tab, 20); for(int j=0; j<20; j++) printf("%d ", tab[j]); return 0;}