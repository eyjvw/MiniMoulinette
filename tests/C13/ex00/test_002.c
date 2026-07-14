#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_btree.h"
int main(void){t_btree *n = btree_create_node((void *)"42");if (!n){printf("NULL");return 0;}printf("[%s]l=%d r=%d", (char *)n->item, n->left == NULL, n->right == NULL);return 0;}
