#include <stdio.h>
void ft_sort_string_tab(char **tab);
int main(void){char *tab[] = {"42", "21", "1337", "", 0};ft_sort_string_tab(tab);for (int i = 0; tab[i]; i++) printf("[%s]", tab[i]);return 0;}
