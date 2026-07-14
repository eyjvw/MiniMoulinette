#include <stdio.h>
char *ft_strcat(char *dest, char *src);
int main(void){char dest[3] = "a"; char src[] = "b";char *r = ft_strcat(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[2] == 0, dest);return 0;}
