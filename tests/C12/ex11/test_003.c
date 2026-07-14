#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
static int cmps(void *a, void *b){return strcmp(a, b);}
t_list *ft_list_find(t_list *begin_list, void *data_ref, int (*cmp)(void *, void *));
int main(void){t_list *l = NULL;t_list *r = ft_list_find(l, (void *)"x", cmps);if (!r) printf("NULL");else printf("[%s]next=%d", (char *)r->data, r->next == NULL);return 0;}
