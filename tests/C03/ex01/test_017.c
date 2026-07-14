#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(){int r = ft_strncmp("HpA1c8q1ROg7XcwCM", "x9F8HGydV9aDGyS i", 2); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}