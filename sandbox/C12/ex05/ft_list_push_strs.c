#include "ft_list.h"

t_list	*ft_list_push_strs(int size, char **strs)
{
	t_list	*begin;
	t_list	*elem;
	int		i;

	begin = 0;
	i = 0;
	while (i < size)
	{
		elem = ft_create_elem(strs[i]);
		if (!elem)
			return (begin);
		elem->next = begin;
		begin = elem;
		i++;
	}
	return (begin);
}
