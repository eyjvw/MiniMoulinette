#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_btree.h"
static t_btree *nd(void *item, t_btree *left, t_btree *right){t_btree *n = malloc(sizeof(t_btree)); n->item = item; n->left = left; n->right = right; return n;}
static int cmps(void *a, void *b){return strcmp(a, b);}
void *btree_search_item(t_btree *root, void *data_ref, int (*cmpf)(void *, void *));
int main(void){t_btree *r = nd("c", nd("b", nd("a", NULL, NULL), NULL), NULL);void *f = btree_search_item(r, (void *)"a", cmps);if (!f) printf("NULL");else printf("[%s]", (char *)f);return 0;}
