#include <stdio.h>
char *ft_strcat(char *dest, char *src);
int main(void){char dest[4] = "abc"; char src[] = "";char *r = ft_strcat(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[3] == 0, dest);return 0;}
