#include <stdio.h>
char *ft_strncat(char *dest, char *src, unsigned int nb);
int main(void){char dest[4] = ""; char *r = ft_strncat(dest, "abc", 3);printf("[%s]", r);return 0;}
