#include <stdio.h>
#include <stdlib.h>
int *ft_map(int *tab, int length, int (*f)(int));
static int inc(int n){return n + 1;}
int main(void){int tab[] = {0, 99, -99, 7}; int *r = ft_map(tab, 4, inc);if (!r && 4 > 0){printf("NULL");return 0;}for (int i = 0; i < 4; i++) printf("%d ", r[i]);printf("$");return 0;}
