#include <stdio.h>
void ft_rev_int_tab(int *tab, int size);
int main(){int tab[]={-89,-38,79,66,-67,-97,-56,61,-88,-22,-76,16,56,-57,51,-84,-73}; ft_rev_int_tab(tab, 17); for(int j=0; j<17; j++) printf("%d ", tab[j]); return 0;}