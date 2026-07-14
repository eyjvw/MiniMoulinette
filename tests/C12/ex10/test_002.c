#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
t_list *mk(void *data, t_list *next);
t_list *mk(void *data, t_list *next){t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next; return n;}
static int cmps(void *a, void *b){return strcmp(a, b);}
void ft_list_foreach_if(t_list *begin_list, void (*f)(void *), void *data_ref, int (*cmp)(void *, void *));
static void pr(void *d){printf("[%s]", (char *)d);}
int main(void){t_list *l = mk("m", mk("m", NULL));ft_list_foreach_if(l, pr, (void *)"m", cmps);printf("$");return 0;}
