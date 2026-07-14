#include <stdio.h>
void ft_foreach(int *tab, int length, void (*f)(int));
static void pr(int n){printf("%d ", n);}
int main(void){int tab[] = {-1, 0, 1, 2147483647, -2147483648}; ft_foreach(tab, 5, pr);printf("$");return 0;}
