#include <stdlib.h>
#include "ft_list.h"

void	ft_list_remove_if(t_list **begin_list, void *data_ref,
		int (*cmp)(void *, void *), void (*free_fct)(void *))
{
	t_list	*cur;

	if (!begin_list)
		return ;
	while (*begin_list && cmp((*begin_list)->data, data_ref) == 0)
	{
		cur = *begin_list;
		*begin_list = cur->next;
		free_fct(cur->data);
		free(cur);
	}
	if (*begin_list)
		ft_list_remove_if(&(*begin_list)->next, data_ref, cmp, free_fct);
}
