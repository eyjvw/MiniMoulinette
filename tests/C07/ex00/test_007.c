#include <stdio.h>
char *ft_strdup(char *src);
int main(void){char s[] = "tab\tnewline\n"; char *d = ft_strdup(s);printf("[%s]", d);return 0;}
