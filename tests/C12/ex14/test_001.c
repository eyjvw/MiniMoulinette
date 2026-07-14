#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
static void plist(t_list *l){while (l){printf("[%s]", (char *)l->data); l = l->next;} printf("$");}
static int cmps(void *a, void *b){return strcmp(a, b);}
void ft_list_sort(t_list **begin_list, int (*cmp)(void *, void *));
int main(void){t_list *l = mk("d", mk("c", mk("b", mk("a", NULL))));ft_list_sort(&l, cmps);plist(l);return 0;}
