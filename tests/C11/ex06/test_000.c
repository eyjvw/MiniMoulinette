#include <stdio.h>
void ft_sort_string_tab(char **tab);
int main(void){char *tab[] = {"banana", "apple", "cherry", 0};ft_sort_string_tab(tab);for (int i = 0; tab[i]; i++) printf("[%s]", tab[i]);return 0;}
