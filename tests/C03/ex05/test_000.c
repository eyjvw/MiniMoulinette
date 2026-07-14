#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[10] = "foo"; unsigned int r = ft_strlcat(dest, "bar", 10);printf("r=%u dest=[%s]", r, dest);return 0;}
