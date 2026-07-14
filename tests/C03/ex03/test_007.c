#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[20] = "12345"; char *r = ft_strncat(dest, "6789", 3);printf("[%s]", r);return 0;}
