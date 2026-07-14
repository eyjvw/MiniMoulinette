#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(){int r = ft_strncmp("V1qlGDyi0M", "V1qlGDyi0M", 10); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}