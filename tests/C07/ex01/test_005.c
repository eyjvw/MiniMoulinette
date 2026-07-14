#include <stdio.h>
int *ft_range(int min, int max);
int main(void){int *r = ft_range(-2147483648, -2147483645);if (!r){printf("NULL");return 0;}for (int i = 0; i < -2147483645 - -2147483648; i++) printf("%d ", r[i]);return 0;}
