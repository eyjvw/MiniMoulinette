#include <stdio.h>
void ft_advanced_sort_string_tab(char **tab, int (*cmp)(char *, char *));
static int cmp_rev(char *a, char *b){int i = 0;while (a[i] && a[i] == b[i]) i++;return (unsigned char)b[i] - (unsigned char)a[i];}
int main(void){char *tab[] = {"Rick", "Morty", "Summer", "Beth", 0};ft_advanced_sort_string_tab(tab, cmp_rev);for (int i = 0; tab[i]; i++) printf("[%s]", tab[i]);return 0;}
