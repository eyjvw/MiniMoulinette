#include <stdio.h>
unsigned int ft_strlcat(char *dest, char *src, unsigned int size);
int main(void){char dest[8] = "aaa"; unsigned int r = ft_strlcat(dest, "bbbbbbbb", 8);printf("r=%u dest=[%s]", r, dest);return 0;}
