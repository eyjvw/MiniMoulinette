#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(){int r = ft_strncmp("HyjN5", "HyjN5", 5); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}