#include <stdio.h>
void ft_foreach(int *tab, int length, void (*f)(int));
static void pr(int n){printf("%d ", n);}
int main(void){int tab[] = {0}; ft_foreach(tab, 0, pr);printf("$");return 0;}
