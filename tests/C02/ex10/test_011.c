#include <stdio.h>
unsigned int ft_strlcpy(char *dest, char *src, unsigned int size);
int main(void){char dest[3]; for (int k = 0; k < 3; k++) dest[k] = 'X';unsigned int r = ft_strlcpy(dest, "cutme", 3);printf("r=%u dest=[%s]", r, dest);return 0;}
