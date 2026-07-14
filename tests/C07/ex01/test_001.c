#include <stdio.h>
int *ft_range(int min, int max);
int main(void){int *r = ft_range(-3, 3);if (!r){printf("NULL");return 0;}for (int i = 0; i < 3 - -3; i++) printf("%d ", r[i]);return 0;}
