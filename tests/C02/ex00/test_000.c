#include <stdio.h>
char *ft_strcpy(char *dest, char *src);
int main(void){char dest[1]; char src[] = "";for (int k = 0; k < 1; k++) dest[k] = 'X';char *r = ft_strcpy(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[0] == 0, dest);return 0;}
