#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_btree.h"
static t_btree *nd(void *item, t_btree *left, t_btree *right){t_btree *n = malloc(sizeof(t_btree)); n->item = item; n->left = left; n->right = right; return n;}
void btree_apply_by_level(t_btree *root, void (*applyf)(void *item, int current_level, int is_first_elem));
static void pl(void *item, int level, int first){printf("(%s,%d,%d)", (char *)item, level, first);}
int main(void){t_btree *r = nd("c", nd("b", nd("a", NULL, NULL), NULL), NULL);btree_apply_by_level(r, pl);printf("$");return 0;}
