#include <stdio.h>
#include <stdlib.h>
int *ft_map(int *tab, int length, int (*f)(int));
static int dbl(int n){return n * 2;}
int main(void){int tab[] = {0}; int *r = ft_map(tab, 0, dbl);if (!r && 0 > 0){printf("NULL");return 0;}for (int i = 0; i < 0; i++) printf("%d ", r[i]);printf("$");return 0;}
