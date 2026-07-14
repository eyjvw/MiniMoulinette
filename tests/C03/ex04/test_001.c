#include <stdio.h>
char *ft_strstr(char *str, char *to_find);
int main(void){char s[] = "Hello World"; char *r = ft_strstr(s, "o W");if (!r) printf("NULL"); else printf("[%s]", r);return 0;}
