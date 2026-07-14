#include <stdio.h>
void ft_foreach(int *tab, int length, void (*f)(int));
static void pr(int n){printf("%d ", n);}
int main(void){int tab[] = {1, 2, 3}; ft_foreach(tab, 3, pr);printf("$");return 0;}
