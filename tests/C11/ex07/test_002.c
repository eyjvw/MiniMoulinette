#include <stdio.h>
void ft_advanced_sort_string_tab(char **tab, int (*cmp)(char *, char *));
static int slen2(char *s){int i = 0; while (s[i]) i++; return i;}
static int cmp_len(char *a, char *b){return slen2(a) - slen2(b);}
int main(void){char *tab[] = {"aaaa", "a", "aa", "aaa", 0};ft_advanced_sort_string_tab(tab, cmp_len);for (int i = 0; tab[i]; i++) printf("[%s]", tab[i]);return 0;}
