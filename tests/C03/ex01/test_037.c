#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(){int r = ft_strncmp("YPKOoIokPSpK4mJtA", "koJg9 PFyZ7J9GGdK", 7); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}