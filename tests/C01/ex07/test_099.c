#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-38,48,-90,-66,-75,61,56,-4,99,-60,-96,24,-80,-99,-99,-55,-78,80,66,51}; ft_rev_int_tab(tab, 20); for(int j=0; j<20; j++) printf("%d ", tab[j]); return 0;}