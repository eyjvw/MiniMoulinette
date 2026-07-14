#include <stdio.h>
#include <stdlib.h>
int *ft_map(int *tab, int length, int (*f)(int));
static int dbl(int n){return n * 2;}
int main(void){int tab[] = {1, 2, 3}; int *r = ft_map(tab, 3, dbl);if (!r && 3 > 0){printf("NULL");return 0;}for (int i = 0; i < 3; i++) printf("%d ", r[i]);printf("$");return 0;}
