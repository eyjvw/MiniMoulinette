#include <stdio.h>
char *ft_strcat(char *dest, char *src);
int main(void){char dest[18] = "prefix-"; char src[] = "suffix end";char *r = ft_strcat(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[17] == 0, dest);return 0;}
