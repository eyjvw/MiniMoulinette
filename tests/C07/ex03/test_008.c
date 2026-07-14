#include <stdio.h>
char *ft_strjoin(int size, char **strs, char *sep);
int main(void){char *arr[] = {"long string here", "another one"}; char *r = ft_strjoin(2, arr, " | ");printf("[%s]", r);return 0;}
