#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[20] = "x"; char *r = ft_strncat(dest, "yyyy", 100);printf("[%s]", r);return 0;}
