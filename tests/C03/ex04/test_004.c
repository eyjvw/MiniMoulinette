#include <stdio.h>
char *ft_strstr(char *str, char *to_find);
int main(void){char s[] = "find me here"; char *r = ft_strstr(s, "");if (!r) printf("NULL"); else printf("[%s]", r);return 0;}
