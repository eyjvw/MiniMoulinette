#include <stdio.h>
char *ft_strjoin(int size, char **strs, char *sep);
int main(void){char *arr[] = {"one"}; char *r = ft_strjoin(1, arr, "XXX");printf("[%s]", r);return 0;}
