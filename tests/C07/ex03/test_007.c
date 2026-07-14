#include <stdio.h>
char *ft_strjoin(int size, char **strs, char *sep);
int main(void){char *arr[] = {"wubba", "lubba", "dub", "dub"}; char *r = ft_strjoin(4, arr, " ");printf("[%s]", r);return 0;}
