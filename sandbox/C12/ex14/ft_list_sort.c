#include "ft_list.h"

void	ft_list_sort(t_list **begin_list, int (*cmp)(void *, void *))
{
	t_list	*cur;
	void	*tmp;
	int		swapped;

	if (!begin_list)
		return ;
	swapped = 1;
	while (swapped)
	{
		swapped = 0;
		cur = *begin_list;
		while (cur && cur->next)
		{
			if (cmp(cur->data, cur->next->data) > 0)
			{
				tmp = cur->data;
				cur->data = cur->next->data;
				cur->next->data = tmp;
				swapped = 1;
			}
			cur = cur->next;
		}
	}
}
