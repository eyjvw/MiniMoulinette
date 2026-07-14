#include <stdio.h>
int ft_strncmp(char *s1, char *s2, unsigned int n);
int main(){int r = ft_strncmp("QLXLA4jTy7Q", "QT8PJsK8xoa", 1); if(r>0)r=1; if(r<0)r=-1; printf("%d", r); return 0;}