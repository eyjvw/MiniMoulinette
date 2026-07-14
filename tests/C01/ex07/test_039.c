#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={77,51,10,100,11,45,-13,39,77,-40,-56,69,71,-81,89,82,46,24,-71,51}; ft_rev_int_tab(tab, 20); for(int j=0; j<20; j++) printf("%d ", tab[j]); return 0;}