#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
int ft_list_size(t_list *begin_list);
int main(void){t_list *l = mk("1", mk("2", mk("3", mk("4", mk("5", mk("6", mk("7", NULL)))))));printf("%d", ft_list_size(l));return 0;}
