#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
static void plist(t_list *l){while (l){printf("[%s]", (char *)l->data); l = l->next;} printf("$");}
static int cmps(void *a, void *b){return strcmp(a, b);}
void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)(void *, void *), void (*free_fct)(void *));
int main(void){t_list *l = NULL;l = mk(strdup("del"), l);l = mk(strdup("keep"), l);ft_list_remove_if(&l, (void *)"del", cmps, free);plist(l);return 0;}
