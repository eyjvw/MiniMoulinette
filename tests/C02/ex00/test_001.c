#include <stdio.h>
char *ft_strcpy(char *dest, char *src);
int main(void){char dest[2]; char src[] = "a";for (int k = 0; k < 2; k++) dest[k] = 'X';char *r = ft_strcpy(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[1] == 0, dest);return 0;}
