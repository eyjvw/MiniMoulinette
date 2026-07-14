#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[20] = "A"; char *r = ft_strncat(dest, "BCDEFG", 6);printf("[%s]", r);return 0;}
