#include "ft_list.h"

static void	insert_node(t_list **begin_list, t_list *node,
		int (*cmp)(void *, void *))
{
	t_list	*cur;

	if (!*begin_list || cmp((*begin_list)->data, node->data) >= 0)
	{
		node->next = *begin_list;
		*begin_list = node;
		return ;
	}
	cur = *begin_list;
	while (cur->next && cmp(cur->next->data, node->data) < 0)
		cur = cur->next;
	node->next = cur->next;
	cur->next = node;
}

void	ft_sorted_list_merge(t_list **begin_list1, t_list *begin_list2,
		int (*cmp)(void *, void *))
{
	t_list	*next;

	if (!begin_list1)
		return ;
	while (begin_list2)
	{
		next = begin_list2->next;
		insert_node(begin_list1, begin_list2, cmp);
		begin_list2 = next;
	}
}
