#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
void ft_list_foreach(t_list *begin_list, void (*f)(void *));
static void pr(void *d){printf("[%s]", (char *)d);}
int main(void){t_list *l = mk("a", mk("b", mk("c", NULL)));ft_list_foreach(l, pr);printf("$");return 0;}
