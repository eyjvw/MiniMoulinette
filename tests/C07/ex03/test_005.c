#include <stdio.h>
char *ft_strjoin(int size, char **strs, char *sep);
int main(void){char *arr[] = {"Rick", "Morty"}; char *r = ft_strjoin(2, arr, "");printf("[%s]", r);return 0;}
