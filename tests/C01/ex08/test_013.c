#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={56,-41,81,-26,-51,-100,-70,-94,19,60,-70,88,-47,57}; ft_sort_int_tab(tab, 14); for(int j=0; j<14; j++) printf("%d ", tab[j]); return 0;}