#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
void ft_list_clear(t_list *begin_list, void (*free_fct)(void *));
static void fr(void *d){printf("F[%s]", (char *)d); free(d);}
int main(void){t_list *l = NULL;l = mk(strdup("only"), l);ft_list_clear(l, fr);printf("$");return 0;}
