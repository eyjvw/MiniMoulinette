#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ft_list.h"
int main(void){t_list *e = ft_create_elem((void *)"");if (!e){printf("NULL");return 0;}printf("[%s]next=%d", (char *)e->data, e->next == NULL);return 0;}
