#include <stdio.h>
void ft_sort_int_tab(int *tab, int size);
int main(){int tab[]={-18,-46,95,-89,51,-56,-15,-84,-70,-30,-64,93,6,-57,78,-6,41,-58,12}; ft_sort_int_tab(tab, 19); for(int j=0; j<19; j++) printf("%d ", tab[j]); return 0;}