#include <stdio.h>
#include <stdlib.h>
int *ft_map(int *tab, int length, int (*f)(int));
static int inc(int n){return n + 1;}
int main(void){int tab[] = {2147483646, -2147483647}; int *r = ft_map(tab, 2, inc);if (!r && 2 > 0){printf("NULL");return 0;}for (int i = 0; i < 2; i++) printf("%d ", r[i]);printf("$");return 0;}
