#include <stdio.h>
int ft_strcmp(char *s1, char *s2);
int main(void){int r = ft_strcmp("42", "42");printf("%d", (r > 0) - (r < 0));return 0;}
