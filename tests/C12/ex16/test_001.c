#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
static void plist(t_list *l){while (l){printf("[%s]", (char *)l->data); l = l->next;} printf("$");}
static int cmps(void *a, void *b){return strcmp(a, b);}
t_list *ft_create_elem(void *data){t_list *e = malloc(sizeof(t_list)); if (!e) return NULL; e->data = data; e->next = NULL; return e;}
void ft_sorted_list_insert(t_list **begin_list, void *data, int (*cmp)(void *, void *));
int main(void){t_list *l = mk("b", mk("d", NULL));ft_sorted_list_insert(&l, (void *)"a", cmps);plist(l);return 0;}
