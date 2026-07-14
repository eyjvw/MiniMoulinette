#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[6] = "tight"; char *r = ft_strncat(dest, "x", 0);printf("[%s]", r);return 0;}
