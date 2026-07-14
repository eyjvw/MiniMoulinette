#include <stdio.h>
char *ft_strcpy(char *dest, char *src);
int main(void){char dest[16]; char src[] = "exact fit here!";for (int k = 0; k < 16; k++) dest[k] = 'X';char *r = ft_strcpy(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[15] == 0, dest);return 0;}
