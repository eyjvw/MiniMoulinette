#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-84,-26,20,-66,-69,77,-30,-16,34,5}; ft_rev_int_tab(tab, 10); for(int j=0; j<10; j++) printf("%d ", tab[j]); return 0;}