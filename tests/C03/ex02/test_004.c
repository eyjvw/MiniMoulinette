#include <stdio.h>
char *ft_strcat(char *dest, char *src);
int main(void){char dest[10] = "42"; char src[] = " school";char *r = ft_strcat(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[9] == 0, dest);return 0;}
