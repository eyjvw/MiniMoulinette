#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[20] = "start"; unsigned int r = ft_strlcat(dest, "-end", 100);printf("r=%u dest=[%s]", r, dest);return 0;}
