#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_btree.h"
static int cmps(void *a, void *b){return strcmp(a, b);}
t_btree *btree_create_node(void *item){t_btree *n = malloc(sizeof(t_btree)); if (!n) return NULL; n->item = item; n->left = NULL; n->right = NULL; return n;}
void btree_insert_data(t_btree **root, void *item, int (*cmpf)(void *, void *));
static void show(t_btree *r){if (!r) return; show(r->left);printf("[%s]", (char *)r->item); show(r->right);}
int main(void){t_btree *r = NULL;btree_insert_data(&r, (void *)"d", cmps);btree_insert_data(&r, (void *)"b", cmps);btree_insert_data(&r, (void *)"f", cmps);btree_insert_data(&r, (void *)"a", cmps);btree_insert_data(&r, (void *)"c", cmps);btree_insert_data(&r, (void *)"e", cmps);btree_insert_data(&r, (void *)"g", cmps); show(r);printf("$");return 0;}
