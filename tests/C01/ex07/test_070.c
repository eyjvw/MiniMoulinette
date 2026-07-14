#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-47,47,87,-12,-87,64,-33,93,-71,-87,-58}; ft_rev_int_tab(tab, 11); for(int j=0; j<11; j++) printf("%d ", tab[j]); return 0;}