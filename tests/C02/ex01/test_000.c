#include <stdio.h>
char *ft_strncpy(char *dest, char *src, unsigned int n);
int main(void){char dest[4]; char src[] = "hello";for (int k = 0; k < 4; k++) dest[k] = 'X';char *r = ft_strncpy(dest, src, 3);printf("ret=%d bytes=", r == dest);for (int k = 0; k < 4; k++) printf("%02x ", (unsigned char)dest[k]);return 0;}
