#include <stdio.h>
char *ft_strjoin(int size, char **strs, char *sep);
int main(void){char *arr[] = {"a", "b", "c", "d"}; char *r = ft_strjoin(4, arr, ", ");printf("[%s]", r);return 0;}
