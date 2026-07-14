#include <stdio.h>
int *ft_range(int min, int max);
int main(void){int *r = ft_range(100, 100);if (!r){printf("NULL");return 0;}for (int i = 0; i < 100 - 100; i++) printf("%d ", r[i]);return 0;}
