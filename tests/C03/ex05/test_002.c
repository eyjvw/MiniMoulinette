#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[10] = ""; unsigned int r = ft_strlcat(dest, "abc", 10);printf("r=%u dest=[%s]", r, dest);return 0;}
