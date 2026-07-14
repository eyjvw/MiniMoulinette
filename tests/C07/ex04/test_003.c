#include <stdio.h>
char *ft_convert_base(char *nbr, char *base_from, char *base_to);
int main(void){char *r = ft_convert_base("255", "0123456789", "0123456789abcdef");if (!r) printf("NULL"); else printf("[%s]", r);return 0;}
