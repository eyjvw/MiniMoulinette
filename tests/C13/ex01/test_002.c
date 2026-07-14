#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_btree.h"
static t_btree *nd(void *item, t_btree *left, t_btree *right){t_btree *n = malloc(sizeof(t_btree)); n->item = item; n->left = left; n->right = right; return n;}
static void pv(void *item){printf("[%s]", (char *)item);}
void btree_apply_prefix(t_btree *root, void (*applyf)(void *));
int main(void){t_btree *r = nd("a", NULL, nd("b", NULL, nd("c", NULL, NULL)));btree_apply_prefix(r, pv);printf("$");return 0;}
