#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[2] = "x"; unsigned int r = ft_strlcat(dest, "yyyy", 2);printf("r=%u dest=[%s]", r, dest);return 0;}
