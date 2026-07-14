#include <stdio.h>
char *ft_strcat(char *dest, char *src);
int main(void){char dest[12] = "Hello "; char src[] = "World";char *r = ft_strcat(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[11] == 0, dest);return 0;}
