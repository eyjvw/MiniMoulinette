#include <stdio.h>
int *ft_range(int min, int max);
int main(void){int *r = ft_range(6, 2);if (!r){printf("NULL");return 0;}for (int i = 0; i < 2 - 6; i++) printf("%d ", r[i]);return 0;}
