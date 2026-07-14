#include <stdio.h>
unsigned int ft_strlcpy(char *dest, char *src, unsigned int size);
int main(void){char dest[40]; for (int k = 0; k < 40; k++) dest[k] = 'X';unsigned int r = ft_strlcpy(dest, "full copy here", 15);printf("r=%u dest=[%s]", r, dest);return 0;}
