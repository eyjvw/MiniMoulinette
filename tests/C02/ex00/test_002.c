#include <stdio.h>
char *ft_strcpy(char *dest, char *src);
int main(void){char dest[6]; char src[] = "hello";for (int k = 0; k < 6; k++) dest[k] = 'X';char *r = ft_strcpy(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[5] == 0, dest);return 0;}
