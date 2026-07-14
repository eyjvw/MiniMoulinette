#include "ft_list.h"

static int	list_size(t_list *lst)
{
	int	n;

	n = 0;
	while (lst)
	{
		n++;
		lst = lst->next;
	}
	return (n);
}

static t_list	*list_at(t_list *lst, int i)
{
	while (i > 0)
	{
		lst = lst->next;
		i--;
	}
	return (lst);
}

void	ft_list_reverse_fun(t_list *begin_list)
{
	int		i;
	int		n;
	void	*tmp;
	t_list	*a;
	t_list	*b;

	n = list_size(begin_list);
	i = 0;
	while (i < n / 2)
	{
		a = list_at(begin_list, i);
		b = list_at(begin_list, n - 1 - i);
		tmp = a->data;
		a->data = b->data;
		b->data = tmp;
		i++;
	}
}
