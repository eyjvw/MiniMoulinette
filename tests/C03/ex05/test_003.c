#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[5] = "full"; unsigned int r = ft_strlcat(dest, "xxxx", 5);printf("r=%u dest=[%s]", r, dest);return 0;}
