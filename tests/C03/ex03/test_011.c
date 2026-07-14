#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[5] = "ab"; char *r = ft_strncat(dest, "cdX", 2);printf("[%s]", r);return 0;}
