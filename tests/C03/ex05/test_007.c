#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[20] = "12345"; unsigned int r = ft_strlcat(dest, "6789", 4);printf("r=%u dest=[%s]", r, dest);return 0;}
