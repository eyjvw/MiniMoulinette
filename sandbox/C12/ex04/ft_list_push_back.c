#include "ft_list.h"

void	ft_list_push_back(t_list **begin_list, void *data)
{
	t_list	*elem;
	t_list	*last;

	elem = ft_create_elem(data);
	if (!elem)
		return ;
	if (!*begin_list)
	{
		*begin_list = elem;
		return ;
	}
	last = *begin_list;
	while (last->next)
		last = last->next;
	last->next = elem;
}
