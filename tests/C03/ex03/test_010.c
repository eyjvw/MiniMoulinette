#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[12] = "Hello "; char *r = ft_strncat(dest, "World", 5);printf("[%s]", r);return 0;}
