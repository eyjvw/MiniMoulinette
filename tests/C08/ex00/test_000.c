#include <unistd.h>
#include "ft.h"
int main(void){int a = 1; int b = 2; ft_swap(&a, &b);ft_putchar('0' + a); ft_putchar('0' + b); ft_putchar('\n');ft_putstr("hi"); ft_putchar('0' + ft_strlen("hello"));ft_putchar('0' + (ft_strcmp("a", "a") == 0));ft_putchar('\n'); return 0;}
void ft_putchar(char c){write(1, &c, 1);}
void ft_putstr(char *s){while (*s) write(1, s++, 1);}
void ft_swap(int *a, int *b){int t = *a; *a = *b; *b = t;}
int ft_strlen(char *s){int i = 0; while (s[i]) i++; return i;}
int ft_strcmp(char *a, char *b){int i = 0;while (a[i] && a[i] == b[i]) i++;return (unsigned char)a[i] - (unsigned char)b[i];}
