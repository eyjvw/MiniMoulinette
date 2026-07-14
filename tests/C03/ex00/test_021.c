#include <stdio.h>
int ft_strcmp(char *s1, char *s2);
int main(){int r = ft_strcmp("8", "V"); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}