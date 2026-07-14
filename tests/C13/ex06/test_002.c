#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_btree.h"
static t_btree *nd(void *item, t_btree *left, t_btree *right){t_btree *n = malloc(sizeof(t_btree)); n->item = item; n->left = left; n->right = right; return n;}
int btree_level_count(t_btree *root);
int main(void){t_btree *r = nd("a", NULL, nd("b", NULL, nd("c", NULL, NULL)));printf("%d", btree_level_count(r));return 0;}
