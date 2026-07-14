#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[20] = "cat"; char *r = ft_strncat(dest, "", 5);printf("[%s]", r);return 0;}
