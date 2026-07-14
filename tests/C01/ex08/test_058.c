#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={75,62,38,48,-21,56,-87,-13,36,99,-98,20,16,31,20,46,87,-16,7}; ft_sort_int_tab(tab, 19); for(int j=0; j<19; j++) printf("%d ", tab[j]); return 0;}