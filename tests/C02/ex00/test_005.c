#include <stdio.h>
char *ft_strcpy(char *dest, char *src);
int main(void){char dest[21]; char src[] = "with\ttab and  spaces";for (int k = 0; k < 21; k++) dest[k] = 'X';char *r = ft_strcpy(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[20] == 0, dest);return 0;}
