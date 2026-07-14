#include <stdio.h>
char *ft_strcpy(char *dest, char *src);
int main(void){char dest[18]; char src[] = "42 school piscine";for (int k = 0; k < 18; k++) dest[k] = 'X';char *r = ft_strcpy(dest, src);printf("ret=%d term=%d [%s]", r == dest, dest[17] == 0, dest);return 0;}
