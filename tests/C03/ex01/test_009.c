#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(void){int r = ft_strncmp("same", "same", 100);printf("%d", (r > 0) - (r < 0));return 0;}
