#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
static void plist(t_list *l){while (l){printf("[%s]", (char *)l->data); l = l->next;} printf("$");}
t_list *ft_create_elem(void *data){t_list *e = malloc(sizeof(t_list)); if (!e) return NULL; e->data = data; e->next = NULL; return e;}
t_list *ft_list_push_strs(int size, char **strs);
int main(void){char *strs[] = {"x", "y", "z", "w"};t_list *l = ft_list_push_strs(4, strs);plist(l);return 0;}
