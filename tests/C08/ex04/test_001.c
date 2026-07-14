#include <stdio.h>
typedef struct s_stock_str{int size;char *str;char *copy;}t_stock_str;
struct s_stock_str *ft_strs_to_tab(int ac, char **av);
int main(void){char *av[] = {"one"}; int ac = 1;t_stock_str *t = ft_strs_to_tab(ac, av);if (!t){printf("NULL");return 0;}for (int i = 0; t[i].str; i++)printf("[%d|%s|%s]", t[i].size, t[i].str, t[i].copy);return 0;}
