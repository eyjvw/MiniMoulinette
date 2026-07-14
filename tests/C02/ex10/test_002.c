#include <stdio.h>
unsigned int ft_strlcpy(char *dest, char *src, unsigned int size);
int main(void){char dest[10]; for (int k = 0; k < 10; k++) dest[k] = 'X';unsigned int r = ft_strlcpy(dest, "", 5);printf("r=%u dest=[%s]", r, dest);return 0;}
