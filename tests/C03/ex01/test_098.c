#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(){int r = ft_strncmp("T4v9cqJfu0bk5rtjhg", "8gYTkw5XG5TRJBWFnx", 8); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}