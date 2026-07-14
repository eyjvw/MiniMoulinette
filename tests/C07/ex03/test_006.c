#include <stdio.h>
char *ft_strjoin(int size, char **strs, char *sep);
int main(void){char *arr[] = {"1", "2", "3"}; char *r = ft_strjoin(3, arr, " + ");printf("[%s]", r);return 0;}
