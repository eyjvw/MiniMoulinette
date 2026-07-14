#include <stdio.h>
int ft_any(char **tab, int (*f)(char *));
int has_a(char *s);
int longer3(char *s);
int is_empty(char *s);
int has_a(char *s){while (*s){if (*s == 'a') return 1; s++;}return 0;}
int longer3(char *s){int i = 0; while (s[i]) i++; return i > 3;}
int is_empty(char *s){return s[0] == '\0';}
int main(void){char *tab[] = {"ab", "cd", "efgh", 0};printf("%d", ft_any(tab, longer3));return 0;}
