#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
t_list *ft_list_at(t_list *begin_list, unsigned int nbr);
int main(void){t_list *l = mk("a", mk("b", mk("c", mk("d", NULL))));t_list *r = ft_list_at(l, 3);if (!r) printf("NULL");else printf("[%s]", (char *)r->data);return 0;}
