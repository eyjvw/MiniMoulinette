#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[20] = "foo"; char *r = ft_strncat(dest, "bar", 10);printf("[%s]", r);return 0;}
