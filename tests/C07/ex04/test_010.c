#include <stdio.h>
char *ft_convert_base(char *nbr, char *base_from, char *base_to);
int main(void){char *r = ft_convert_base("42", "00", "0123456789");if (!r) printf("NULL"); else printf("[%s]", r);return 0;}
