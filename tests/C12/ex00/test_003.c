#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
int main(void){t_list *e = ft_create_elem(NULL);if (!e){printf("NULL");return 0;}printf("data=%d next=%d", e->data == NULL, e->next == NULL);return 0;}
