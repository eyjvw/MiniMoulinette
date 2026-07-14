#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
static void plist(t_list *l){while (l){printf("[%s]", (char *)l->data); l = l->next;} printf("$");}
t_list *ft_create_elem(void *data){t_list *e = malloc(sizeof(t_list)); if (!e) return NULL; e->data = data; e->next = NULL; return e;}
void ft_list_push_front(t_list **begin_list, void *data);
int main(void){t_list *l = NULL;ft_list_push_front(&l, (void *)"x");ft_list_push_front(&l, (void *)"y");ft_list_push_front(&l, (void *)"z");ft_list_push_front(&l, (void *)"w");ft_list_push_front(&l, (void *)"v"); plist(l);return 0;}
