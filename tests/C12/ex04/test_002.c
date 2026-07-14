#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
static void plist(t_list *l){while (l){printf("[%s]", (char *)l->data); l = l->next;} printf("$");}
t_list *ft_create_elem(void *data){t_list *e = malloc(sizeof(t_list)); if (!e) return NULL; e->data = data; e->next = NULL; return e;}
void ft_list_push_back(t_list **begin_list, void *data);
int main(void){t_list *l = NULL;ft_list_push_back(&l, (void *)"1");ft_list_push_back(&l, (void *)"2");ft_list_push_back(&l, (void *)"3");ft_list_push_back(&l, (void *)"4"); plist(l);return 0;}
