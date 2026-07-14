#include <stdio.h>
void ft_foreach(int *tab, int length, void (*f)(int));
static void pr(int n){printf("%d ", n);}
int main(void){int tab[] = {9, -9, 8, -8, 7}; ft_foreach(tab, 5, pr);printf("$");return 0;}
