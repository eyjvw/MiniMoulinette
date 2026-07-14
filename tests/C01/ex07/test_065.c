#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={57,-29,-30,-35,-97,89}; ft_rev_int_tab(tab, 6); for(int j=0; j<6; j++) printf("%d ", tab[j]); return 0;}