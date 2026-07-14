#include <stdio.h>
char *ft_strstr(char *str, char *to_find);
int main(void){char s[] = "aaa"; char *r = ft_strstr(s, "aa");if (!r) printf("NULL"); else printf("[%s]", r);return 0;}
