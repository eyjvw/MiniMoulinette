#include <stdio.h>
char *ft_strjoin(int size, char **strs, char *sep);
int main(void){char **arr = (void *)0; char *r = ft_strjoin(0, arr, "sep");printf("[%s]", r);return 0;}
