#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(){int r = ft_strncmp("7hLDdUiEri1H1vkiuY", "3kL7BXaYC zqkZeU5d", 3); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}