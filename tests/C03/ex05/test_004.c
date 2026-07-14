#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[20] = "abc"; unsigned int r = ft_strlcat(dest, "", 20);printf("r=%u dest=[%s]", r, dest);return 0;}
