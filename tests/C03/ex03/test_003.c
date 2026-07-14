#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[20] = "start"; char *r = ft_strncat(dest, "-end", 2);printf("[%s]", r);return 0;}
