#include <stdio.h>
char *ft_strncpy(char *dest, char *src, unsigned int n);
int main(void){char dest[2]; char src[] = "abc";for (int k = 0; k < 2; k++) dest[k] = 'X';char *r = ft_strncpy(dest, src, 0);printf("ret=%d bytes=", r == dest);for (int k = 0; k < 2; k++) printf("%02x ", (unsigned char)dest[k]);return 0;}
