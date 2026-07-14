#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[20] = ""; char *r = ft_strncat(dest, "full", 4);printf("[%s]", r);return 0;}
