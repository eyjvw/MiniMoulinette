#include <stdio.h>
char *ft_strcpy(char *dest, char *src);
int main(void){char dest[61]; char src[] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";for (int k = 0; k < 61; k++) dest[k] = 'X';char *r = ft_strcpy(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[60] == 0, dest);return 0;}
