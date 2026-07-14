#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
static void plist(t_list *l){while (l){printf("[%s]", (char *)l->data); l = l->next;} printf("$");}
static int cmps(void *a, void *b){return strcmp(a, b);}
void ft_sorted_list_merge(t_list **begin_list1, t_list *begin_list2, int (*cmp)(void *, void *));
int main(void){t_list *l1 = mk("a", mk("c", mk("e", NULL))); t_list *l2 = mk("b", mk("d", mk("f", NULL)));ft_sorted_list_merge(&l1, l2, cmps);plist(l1);return 0;}
